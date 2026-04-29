import json
import logging
import re
import xml.etree.ElementTree as ET
from os.path import abspath
from xml.dom import minidom

import requests

from constants import dcatNamespaces, fallbackLanguages, fullnameSwaps, schNamespaces, uriSwaps, primaryLanguage


LANGUAGE_CODE_ALIASES = {
    'dut': 'nl',
    'nld': 'nl',
    'eng': 'en',
    'fre': 'fr',
    'fra': 'fr',
    'ger': 'de',
    'deu': 'de'
}


def _applyUriSwap(uri):
    if not isinstance(uri, str):
        return uri

    if uri in uriSwaps:
        return uriSwaps[uri]

    for source, target in uriSwaps.items():
        if uri.startswith(source):
            return target + uri[len(source):]

    return uri


def loadJsonUrl(url):
    content_type = ''
    text = ''
    if url.startswith('http://') or url.startswith('https://'):
        response = requests.get(url)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', '')
        text = response.text
    else:
        file_path = abspath(url)
        logging.debug('Reading file ' + file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

    if _isTurtleSource(url, content_type):
        logging.debug('Converting Turtle source to JSON-LD: %s', url)
        text = convertTurtleToJsonLd(text, url)

    return json.loads(text)


def _isTurtleSource(url, content_type):
    lower_url = url.lower().split('?', 1)[0]
    lower_type = content_type.lower()
    return lower_url.endswith('.ttl') or \
        lower_url.endswith('.turtle') or \
        'text/turtle' in lower_type or \
        'application/x-turtle' in lower_type


def convertTurtleToJsonLd(ttl_text, source=''):
    try:
        from rdflib import Graph
    except ImportError as err:
        raise ImportError('rdflib is required to convert Turtle SHACL files to JSON-LD') from err

    graph = Graph()
    graph.parse(data=ttl_text, format='turtle', publicID=source if source else None)
    jsonld_text = graph.serialize(format='json-ld', indent=2)
    return jsonld_text.decode('utf-8') if isinstance(jsonld_text, bytes) else jsonld_text


def getFullName(uri, source=None):
    if not isinstance(uri, str):
        logging.error(
            'getFullName expected str but received %s: %r',
            type(uri).__name__,
            uri
        )
        raise TypeError(
            'getFullName expected uri as str, got {0}: {1!r}'.format(type(uri).__name__, uri)
        )

    uri = _applyUriSwap(uri)
    source_hint = '' if source is None else ' (source: {0})'.format(source)

    # Blank nodes are not valid QName targets for Schematron/XPath contexts.
    if uri.startswith('_:'):
        logging.error(
            'Blank node identifier {0!r} cannot be converted to a QName{1}. '
            'This usually means a JSON-LD @id reference was not resolved during normalization.'.format(uri, source_hint)
        )
        return uri

    # Already a compact prefixed name (e.g. "dct:issued")
    if ':' in uri and '://' not in uri:
        return fullnameSwaps.get(uri, uri)

    fullname = None
    for ns, nsUri in (list(dcatNamespaces.items()) + list(schNamespaces.items())):
        if str.startswith(uri, nsUri):
            fullname = ns + ':' + uri[len(nsUri):]
            break

    if fullname is not None:
        if fullname in fullnameSwaps:
            return fullnameSwaps[fullname]
        else:
            return fullname
    else:
        raise Exception('Could not find namespace for uri ' + uri + '. Add its namespace to constants.py.')


def safeRemove(arr, elem):
    if elem in arr:
        arr.remove(elem)


def schEl(ns, name):
    if ns not in schNamespaces:
        raise Exception(ns + ' not found in configured schematron namespaces')
    return ET.Element(ET.QName(schNamespaces[ns], name))


def schSubEl(el, ns, name):
    if ns not in schNamespaces:
        raise Exception(ns + ' not found in configured schematron namespaces')
    return ET.SubElement(el, ET.QName(schNamespaces[ns], name))


def addLet(rule, varName, value):
    let = schSubEl(rule, 'sch', 'let')
    let.set('name', varName)
    let.set('value', value)


def swapURI(uri):
    return uriSwaps[uri] if uri in uriSwaps else uri


def writeXmlToFile(element, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(prettyPrintXml(element))


def prettyPrintXml(element):
    xmlStr = ET.tostring(element, xml_declaration=True, encoding='utf-8')
    prettyStr = minidom.parseString(xmlStr).toprettyxml(indent=' ' * 2, encoding='utf-8', newl="\n").decode('utf-8')
    lines = prettyStr.split('\n')
    lines = filter(lambda line: line.strip() != '', lines)
    return '\n'.join(lines)


def castArray(var):
    if not isinstance(var, list):
        var = [var]
    return var


def getLanguageValue(source, propertyName=None, preferredLanguage=None, fallbackLangs=None, default=''):
    if propertyName is not None:
        if not isinstance(source, dict) or propertyName not in source:
            return default
        source = source[propertyName]

    if source is None:
        return default

    if isinstance(source, str):
        return source

    if isinstance(source, dict):
        preferredLanguage = primaryLanguage if preferredLanguage is None else preferredLanguage
        fallbackLangs = fallbackLanguages if fallbackLangs is None else fallbackLangs

        if preferredLanguage in source and isinstance(source[preferredLanguage], str):
            return source[preferredLanguage]

        for lang in fallbackLangs:
            if lang in source and isinstance(source[lang], str):
                return source[lang]

        for value in source.values():
            if isinstance(value, str):
                return value

    return str(source) if source != '' else default


def normalizeLanguageCode(languageCode):
    if not isinstance(languageCode, str) or languageCode.strip() == '':
        return ''

    normalized = languageCode.strip().lower().replace('_', '-')
    if normalized in LANGUAGE_CODE_ALIASES:
        return LANGUAGE_CODE_ALIASES[normalized]

    # Keep regional variants (for example nl-be) under their base language.
    base = normalized.split('-', 1)[0]
    return LANGUAGE_CODE_ALIASES.get(base, base)


def getLanguageValues(source, propertyName=None, defaultLanguage=None):
    if propertyName is not None:
        if not isinstance(source, dict) or propertyName not in source:
            return {}
        source = source[propertyName]

    if source is None:
        return {}

    normalized_default = normalizeLanguageCode(defaultLanguage or primaryLanguage)

    if isinstance(source, str):
        text = source.strip()
        if text == '':
            return {}
        return {normalized_default if normalized_default != '' else 'und': text}

    if isinstance(source, dict):
        localized = {}
        for lang, value in source.items():
            if not isinstance(value, str):
                continue
            text = value.strip()
            if text == '':
                continue

            normalized_lang = normalizeLanguageCode(lang)
            key = normalized_lang if normalized_lang != '' else (normalized_default if normalized_default != '' else 'und')

            if key not in localized:
                localized[key] = text
        return localized

    text = str(source).strip()
    if text == '':
        return {}

    return {normalized_default if normalized_default != '' else 'und': text}


def _collapseIri(iri):
    """Convert a full IRI to a compact prefixed name using known namespaces, or return it as-is."""
    # TODO: Check if strict check is needed. We may generate sch rules with bad XPath in such case.
    #    if isinstance(iri, str) and iri.startswith('_:'):
    #     raise ValueError(
    #         'Blank node identifier {0!r} leaked into IRI compaction (_collapseIri). '
    #         'Normalization should resolve SHACL references before QName conversion.'.format(iri)
    #     )

    iri = _applyUriSwap(iri)
    for ns, nsUri in (list(dcatNamespaces.items()) + list(schNamespaces.items())):
        if iri.startswith(nsUri):
            compact = ns + ':' + iri[len(nsUri):]
            return fullnameSwaps.get(compact, compact)
    return iri


def _extractJsonLdValue(values):
    """
    Normalise a JSON-LD value array to a plain Python value:
    - list of language-tagged strings  -> {lang: value} dict  (e.g. sh:name)
    - single {@id: iri}                -> compact prefixed name
    - single {@value: x}               -> str(x)
    - anything else                    -> returned unchanged
    """
    if not isinstance(values, list):
        return values

    # Language-tagged strings -> language map
    if values and all(isinstance(v, dict) and '@language' in v for v in values):
        return {v['@language']: v['@value'] for v in values}

    # Single IRI reference
    if len(values) == 1 and isinstance(values[0], dict) and '@id' in values[0]:
        return _collapseIri(values[0]['@id'])

    # Single plain literal
    if len(values) == 1 and isinstance(values[0], dict) and '@value' in values[0]:
        return str(values[0]['@value'])

    # Multiple IRI references
    if all(isinstance(v, dict) and '@id' in v for v in values):
        return [_collapseIri(v['@id']) for v in values]

    return values


def normalizeExpandedNode(node):
    """
    Convert an expanded JSON-LD node (full IRI keys + value arrays) to compact
    form (prefixed keys + plain Python values) so SchematronRule can process it
    the same way it handles compacted JSON-LD sources.

    Special JSON-LD keys (@id, @type, @value, @language) are preserved unchanged.
    """
    result = {}
    for key, value in node.items():
        if key.startswith('@'):
            result[key] = value  # keep @id, @type etc. as-is
        else:
            compact_key = _collapseIri(key)
            result[compact_key] = _extractJsonLdValue(value)
    return result


_translation_cache = {}
_qname_pattern = re.compile(r'\b[a-zA-Z_][\w.-]*:[a-zA-Z_][\w.-]*\b')
_qname_placeholder_template = '__GN_QNAME_{0}__'
_qname_placeholder_recovery_pattern = re.compile(
    r'_*(?:(?:__)?GN[_\s-]*QNAME[_\s-]*(\d+)(?:__)?|ZZ\s*QNAME\s*(\d+)\s*ZZ)_*',
    flags=re.IGNORECASE
)


def _protectTechnicalTokens(text):
    """Replace QName-like technical tokens with placeholders before translation."""
    tokens = []

    def _replace(match):
        token = match.group(0)
        placeholder = _qname_placeholder_template.format(len(tokens))
        tokens.append(token)
        return placeholder

    protected = _qname_pattern.sub(_replace, text)
    return protected, tokens


def _restoreTechnicalTokens(text, tokens):
    def _replace(match):
        raw_index = match.group(1) if match.group(1) is not None else match.group(2)
        idx = int(raw_index)
        return tokens[idx] if 0 <= idx < len(tokens) else match.group(0)

    return _qname_placeholder_recovery_pattern.sub(_replace, text)


def _hasUnresolvedTechnicalTokens(text):
    if not isinstance(text, str):
        return False
    return _qname_placeholder_recovery_pattern.search(text) is not None


def translateText(text, targetLanguage='en', sourceLanguage='nl'):
    """
    Translate text using argostranslate (power behind LibreTranslate).
    Results are cached to avoid redundant API calls.

    Args:
        text: Text to translate
        targetLanguage: Target language code (e.g., 'en', 'fr', 'de')
        sourceLanguage: Source language code (default 'nl')

    Returns:
        Translated text, or original text if translation fails or models not installed.

    Note:
        Requires argostranslate language models to be installed.
        Install with argospm, for example:
        argospm install translate-en_nl translate-en_fr translate-en_de
    """
    if not text or not isinstance(text, str) or targetLanguage == sourceLanguage:
        return text

    cache_key = (text, targetLanguage, sourceLanguage)
    if cache_key in _translation_cache:
        return _translation_cache[cache_key]

    try:
        import argostranslate.translate
        logging.getLogger('argostranslate').setLevel(logging.WARNING)
        logging.getLogger('argostranslate.utils').setLevel(logging.WARNING)

        # Keep namespace-prefixed tokens such as dct:title or mdcat:levensfase intact.
        protected_text, protected_tokens = _protectTechnicalTokens(text)

        def _translate(src_text, src_lang, dst_lang):
            return argostranslate.translate.translate(src_text, src_lang, dst_lang)

        if sourceLanguage == 'nl' and targetLanguage in ['fr', 'de']:
            intermediate = _translate(protected_text, 'nl', 'en')
            translated = _translate(intermediate, 'en', targetLanguage)
        else:
            translated = _translate(protected_text, sourceLanguage, targetLanguage)

        translated = _restoreTechnicalTokens(translated, protected_tokens)

        if _hasUnresolvedTechnicalTokens(translated):
            logging.debug('Translation left unresolved technical placeholders. Using source text: "%s"', text[:60])
            translated = text

        _translation_cache[cache_key] = translated
        logging.debug('Translated "%s" to %s: "%s"', text[:30], targetLanguage, translated[:30])
        return translated
    except Exception as err:
        logging.debug(
            'Translation to %s failed for "%s": %s. Using original text. '
            '(Hint: Install models with argospm, eg translate-en_nl translate-en_fr translate-en_de)',
            targetLanguage, text[:30], str(err)
        )
        _translation_cache[cache_key] = text
        return text




