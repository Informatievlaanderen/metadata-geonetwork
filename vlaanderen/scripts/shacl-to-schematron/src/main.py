import logging
import xml.etree.ElementTree as ET

from SchematronGenerator import SchematronGenerator
from SchematronRule import SchematronRule
from constants import shaclSpecsConfig, schNamespaces
from utilities import loadJsonUrl, castArray, getFullName, normalizeExpandedNode


SHACL_NODE_SHAPE = 'http://www.w3.org/ns/shacl#NodeShape'
SHACL_PROPERTY = 'http://www.w3.org/ns/shacl#property'
SHACL_TARGET_CLASS = 'http://www.w3.org/ns/shacl#targetClass'
SHACL_TARGET_OBJECTS_OF = 'http://www.w3.org/ns/shacl#targetObjectsOf'
SHACL_SEVERITY = 'http://www.w3.org/ns/shacl#severity'


def configureLogger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-5s - %(message)s'
    )


def registerNamespaces():
    for ns in schNamespaces:
        ET.register_namespace(ns, schNamespaces[ns])


def generateFromSpec(config):
    stats = {
        'profile': config.get('profile', ''),
        'specUrls': 0,
        'candidates': 0,
        'processed': 0,
        'cardinalityProcessed': 0,
        'skipped': 0,
        'skippedNoTarget': 0,
        'skippedMissingPropertyRef': 0,
        'skippedInvalidSpec': 0
    }

    logging.info('=== Profile start: %s (%s), severity: %s ===', config['name'],
                 config.get('profile', 'no-profile'),
                 config.get('level', 'no-level')
                 )
    cardinalityOnly = bool(config.get('cardinalityOnly', False))
    enableTranslation = bool(config.get('enableTranslation', False))

    schematron = SchematronGenerator(
        config['name'],
        config['title'],
        config['profile'],
        condition=config.get('condition'),
        enableTranslation=enableTranslation
    ) if not cardinalityOnly else None

    cardinalitySchematron = SchematronGenerator(
        config['name'] if cardinalityOnly else _getCardinalitySchematronName(config),
        config['title'],
        config['profile'],
        includeCardinalityAbstract=True,
        schematronTitle=config.get('cardinalityTitle'),
        condition=config.get('condition'),
        enableTranslation=enableTranslation
    ) if cardinalityOnly else None
    hasCardinalityRules = False
    for url in castArray(config['url']):
        stats['specUrls'] += 1
        logging.info('Loading spec: %s', url)
        spec = loadJsonUrl(url)
        # Accept either a dict with `shapes` or a top-level array of shapes.
        # This was the format used in initial JSON-LD files.
        if isinstance(spec, dict) and spec.get('shapes') is not None:
            shapes = spec['shapes']
            for shape in shapes:
                if not hasTarget(shape):
                    stats['skippedNoTarget'] += 1
                    logging.debug('  * Skipping shape without target: %s', shape.get('@id', '<unknown>'))
                    continue

                targetClass = getTargetClass(shape)
                for prop in shape['sh:property']:
                    stats['candidates'] += 1
                    rule = SchematronRule(
                        prop,
                        targetClass,
                        bool(config['profile'])
                    )

                    if cardinalityOnly:
                        if rule.isCardinalityRule():
                            hasCardinalityRules = True
                            stats['processed'] += 1
                            stats['cardinalityProcessed'] += 1
                            cardinalitySchematron.addCardinalityRule(rule)
                        else:
                            stats['skipped'] += 1
                    elif shouldBeAdded(config, prop):
                        stats['processed'] += 1
                        schematron.addRule(rule)
                    else:
                        stats['skipped'] += 1
        # If ttl are converted to JSON-LD, then we have an array
        elif isinstance(spec, list):
            for shape, properties in resolveNodeShapesAndProperties(spec, stats):
                targetClass = getTargetClass(shape)
                logging.debug(' * Shape %s (target: %s)', shape.get('rdfs:label', '<unknown>'), targetClass)
                for prop in properties:
                    stats['candidates'] += 1
                    rule = SchematronRule(
                        prop,
                        targetClass,
                        bool(config['profile'])
                    )
                    isCardinality = rule.isCardinalityRule()
                    logging.debug('   * Property %s (severity: %s, isCardinality: %s)', prop.get('sh:path'), prop.get('sh:severity'), isCardinality)

                    if cardinalityOnly:
                        if isCardinality:
                            hasCardinalityRules = True
                            stats['processed'] += 1
                            stats['cardinalityProcessed'] += 1
                            cardinalitySchematron.addCardinalityRule(rule)
                        else:
                            stats['skipped'] += 1
                    elif shouldBeAdded(config, prop):
                        stats['processed'] += 1
                        schematron.addRule(rule)
                    else:
                        stats['skipped'] += 1
        else:
            logging.warning('Skipping spec without shapes array: %s (type=%s)', url, type(spec).__name__)
            stats['skippedInvalidSpec'] += 1
            continue

    if schematron is not None:
        schematron.generateSchematron()
        schematron.generateLocFiles()

    if cardinalityOnly and hasCardinalityRules:
        cardinalitySchematron.generateSchematron()
        cardinalitySchematron.generateLocFiles()
    logging.info(
        '=== Profile done: %s | urls=%d candidates=%d processed=%d cardinality=%d/%d skipped=%d (no-target=%d missing-ref=%d invalid-spec=%d) ===',
        config['name'],
        stats['specUrls'],
        stats['candidates'],
        stats['processed'],
        stats['cardinalityProcessed'],
        stats['processed'],
        stats['skipped'],
        stats['skippedNoTarget'],
        stats['skippedMissingPropertyRef'],
        stats['skippedInvalidSpec']
    )
    return stats


def shouldBeAdded(config, prop):
    severity = getSeverity(prop)
    # TODO: Check severity can be sh:Info, sh:Violation, sh:Warning?
    return ('level' in config and severity is not None and severity == config['level']) or \
        ('level' not in config and severity is None)
        # ('level' not in config and severity is None)


def getSeverity(prop):
    if 'sh:severity' in prop:
        return prop['sh:severity']

    if SHACL_SEVERITY in prop:
        severity = castArray(prop[SHACL_SEVERITY])
        if len(severity) > 0 and isinstance(severity[0], dict) and '@id' in severity[0]:
            return getFullName(severity[0]['@id'], 'sh:severity')
        if len(severity) > 0 and isinstance(severity[0], str):
            return getFullName(severity[0], 'sh:severity')

    return None


def resolveNodeShapesAndProperties(spec, stats=None):
    by_id = {node.get('@id'): node for node in spec if isinstance(node, dict) and '@id' in node}
    for node in spec:
        if not isinstance(node, dict):
            continue

        if not isNodeShape(node):
            continue

        # Skip anonymous blank-node shapes and shapes without a target class/property
        if not hasTarget(node):
            if stats is not None:
                stats['skippedNoTarget'] += 1
            logging.debug('Skipping NodeShape without target class: %s', node.get('@id', '<unknown>'))
            continue

        properties = []
        for ref in castArray(node.get(SHACL_PROPERTY, [])):
            prop_id = ref.get('@id') if isinstance(ref, dict) else ref
            if prop_id in by_id:
                properties.append(normalizeNodeWithRefs(by_id[prop_id], by_id))
            else:
                if stats is not None:
                    stats['skippedMissingPropertyRef'] += 1
                logging.warning('Property reference %s not found in spec list', prop_id)

        yield normalizeNodeWithRefs(node, by_id), properties


def normalizeNodeWithRefs(node, by_id, visited=None):
    visited = set() if visited is None else visited
    node_id = node.get('@id') if isinstance(node, dict) else None
    if node_id is not None:
        if node_id in visited:
            return normalizeExpandedNode(node)
        visited.add(node_id)

    normalized = normalizeExpandedNode(node)
    for key in ['sh:node', 'sh:property', 'sh:or']:
        if key in normalized:
            normalized[key] = _resolveNodeRefValue(normalized[key], by_id, visited)

    return normalized


def _resolveNodeRefValue(value, by_id, visited):
    if isinstance(value, str):
        return normalizeNodeWithRefs(by_id[value], by_id, set(visited)) if value in by_id else value

    if isinstance(value, dict):
        if '@list' in value:
            return _resolveNodeRefValue(value['@list'], by_id, visited)
        ref_id = value.get('@id')
        return normalizeNodeWithRefs(by_id[ref_id], by_id, set(visited)) if ref_id in by_id else value

    if isinstance(value, list):
        resolved = [_resolveNodeRefValue(item, by_id, visited) for item in value]
        return resolved[0] if len(resolved) == 1 else resolved

    return value


def isNodeShape(node):
    node_types = castArray(node.get('@type', []))
    return SHACL_NODE_SHAPE in node_types


def hasTarget(node):
    """Return True if a NodeShape has sh:targetClass or sh:targetObjectsOf (expanded or compact)."""
    return (
        node.get('sh:targetClass') is not None or
        node.get('sh:targetObjectsOf') is not None or
        SHACL_TARGET_CLASS in node or
        SHACL_TARGET_OBJECTS_OF in node
    )


def getTargetClass(shape):
    target_objects_of = shape.get('sh:targetObjectsOf')
    target_classes_raw = shape.get('sh:targetClass')

    if target_objects_of is None and target_classes_raw is None:
        raise Exception('Target class could not be found in shape {0}'.format(shape.get('@id', '<unknown>')))

    prefix = ''
    if target_objects_of is not None:
        prefix = getFullName(target_objects_of, 'sh:targetObjectsOf') + '/'

    if target_classes_raw is not None:
        raw_list = castArray(target_classes_raw)
        classes = [getFullName(tc, 'sh:targetClass') for tc in raw_list]
    else:
        classes = ['*']

    return [prefix + c for c in classes] if prefix else classes


def _getCardinalitySchematronName(config):
    if 'cardinalityName' in config and config['cardinalityName']:
        return config['cardinalityName']

    base_name = config['name']
    if base_name.endswith('-rec'):
        return base_name[:-4] + '-cardinalities-rec'
    return base_name + '-cardinalities'


if __name__ == '__main__':
    configureLogger()
    registerNamespaces()
    globalStats = {
        'profiles': 0,
        'specUrls': 0,
        'candidates': 0,
        'processed': 0,
        'cardinalityProcessed': 0,
        'skipped': 0,
        'skippedNoTarget': 0,
        'skippedMissingPropertyRef': 0,
        'skippedInvalidSpec': 0
    }

    for specConfig in shaclSpecsConfig:
        profileStats = generateFromSpec(specConfig)
        globalStats['profiles'] += 1
        globalStats['specUrls'] += profileStats['specUrls']
        globalStats['candidates'] += profileStats['candidates']
        globalStats['processed'] += profileStats['processed']
        globalStats['cardinalityProcessed'] += profileStats['cardinalityProcessed']
        globalStats['skipped'] += profileStats['skipped']
        globalStats['skippedNoTarget'] += profileStats['skippedNoTarget']
        globalStats['skippedMissingPropertyRef'] += profileStats['skippedMissingPropertyRef']
        globalStats['skippedInvalidSpec'] += profileStats['skippedInvalidSpec']

    logging.info(
        'Conversion finished | profiles=%d urls=%d candidates=%d processed=%d cardinality=%d/%d skipped=%d (no-target=%d missing-ref=%d invalid-spec=%d)',
        globalStats['profiles'],
        globalStats['specUrls'],
        globalStats['candidates'],
        globalStats['processed'],
        globalStats['cardinalityProcessed'],
        globalStats['processed'],
        globalStats['skipped'],
        globalStats['skippedNoTarget'],
        globalStats['skippedMissingPropertyRef'],
        globalStats['skippedInvalidSpec']
    )
