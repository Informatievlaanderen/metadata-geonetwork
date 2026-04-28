import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from os.path import isfile

from constants import dcatNamespaces, enableTranslation, locOutput, schOutput, schNamespaces, primaryLanguage
from utilities import addLet, writeXmlToFile, schEl, schSubEl, translateText


class SchematronGenerator:

    def __init__(self, name, title, profile=None, includeCardinalityAbstract=False):
        self.name = name
        self.title = title
        self.profile = profile
        self.includeCardinalityAbstract = includeCardinalityAbstract
        self.locKeyPrefix = self._getLocKeyPrefix()
        self.rules = self._getDefaultRules()
        if self.includeCardinalityAbstract:
            self.rules.append(self._buildCardinalityAbstractPattern())
        self.locEntries = self._getDefaultLocEntries()
        self._patternTitleIndex = 1
        self._patternAssertIndex = 1
        self._patternReportIndex = 1

    def addRule(self, rule):
        rulePattern = rule.getPatternElement()
        if rulePattern is not None:
            self.rules.append(rulePattern)

    def addCardinalityRule(self, rule):
        rulePattern = rule.getCardinalityPatternElement()
        # logging.debug('     * Add cardinality rule %s', ET.tostring(rulePattern))
        if rulePattern is not None:
            self.rules.append(rulePattern)

    def generateSchematron(self):
        root = schEl('sch', 'schema')

        for dcatNs in dcatNamespaces:
            nsEl = schSubEl(root, 'sch', 'ns')
            nsEl.set('prefix', dcatNs)
            nsEl.set('uri', dcatNamespaces[dcatNs])

        title = schSubEl(root, 'sch', 'title')
        title.set('xmlns', 'http://www.w3.org/2001/XMLSchema')
        title.text = '{$loc/strings/schematron.title}'

        if self.profile is not None:
            addLet(root, 'profile', 'boolean(//dcat:CatalogRecord//dct:Standard/@rdf:about = \'{0}\')'.format(self.profile))

        for rule in self.rules:
            root.append(rule)

        self._externalizeRuleText(root)

        Path(schOutput).mkdir(parents=True, exist_ok=True)
        writeXmlToFile(root, Path(schOutput + '/' + self.name + '.sch').resolve())

    def generateLocFiles(self):
        _langMap = {'dut': 'nl', 'eng': 'en', 'fre': 'fr', 'ger': 'de'}

        if not enableTranslation:
            logging.debug('Translation disabled by configuration; localization files will use source text for all locales.')

        for loc in self.title:
            Path(locOutput + '/' + loc).mkdir(parents=True, exist_ok=True)
            root = ET.Element('strings')
            locTitle = ET.SubElement(root, 'schematron.title')
            locTitle.text = self.title[loc]

            lang_code = _langMap.get(loc, loc)
            primary_lang = _langMap.get(primaryLanguage, primaryLanguage)

            for key in sorted(self.locEntries.keys()):
                locEl = ET.SubElement(root, key)
                text = self.locEntries[key]

                # Translate if target language differs from primary
                if enableTranslation and lang_code != primary_lang:
                    translated = translateText(text, targetLanguage=lang_code, sourceLanguage=primary_lang)
                    locEl.text = translated
                else:
                    locEl.text = text

            writeXmlToFile(root, Path(locOutput + '/' + loc + '/' + self.name + '.xml').resolve())

    def _externalizeRuleText(self, root):
        for pattern in root.findall('sch:pattern', schNamespaces):
            if pattern.get('abstract') == 'true':
                continue

            for title in pattern.findall('sch:title', schNamespaces):
                self._localizeElementText(title, 'pattern.title', '_patternTitleIndex')

            rule = pattern.find('sch:rule', schNamespaces)
            if rule is None:
                continue

            for assertEl in rule.findall('sch:assert', schNamespaces):
                self._localizeElementText(assertEl, 'pattern.assert', '_patternAssertIndex')

            for reportEl in rule.findall('sch:report', schNamespaces):
                self._localizeElementText(reportEl, 'pattern.report', '_patternReportIndex')

    def _localizeElementText(self, element, keyPrefix, counterName):
        if element.text is None:
            return

        text = element.text.strip()
        if text == '' or text.startswith('$loc/strings/'):
            return

        currentIndex = getattr(self, counterName)
        key = '{0}.{1}.{2}'.format(self.locKeyPrefix, keyPrefix, currentIndex)
        self.locEntries[key] = text
        element.text = '$loc/strings/{0}'.format(key)
        setattr(self, counterName, currentIndex + 1)

    def _getLocKeyPrefix(self):
        return self.name.replace('schematron-rules-', '', 1)

    def _getDefaultRules(self):
        filename = Path('custom_rules/' + self.name + '.sch').resolve()
        return ET.parse(filename).findall('sch:pattern', schNamespaces) if isfile(filename) else []

    def _getDefaultLocEntries(self):
        if not self.includeCardinalityAbstract:
            return {}

        return {
            'cardinality.title': 'Cardinality check (#context / #element)',
            'cardinality.assert': 'Expected cardinality for #element in #context is between #min and #max, found #nodecount.',
            'cardinality.report': 'Cardinality for #element in #context is between #min and #max (#nodecount found).'
        }

    def _buildCardinalityAbstractPattern(self):
        pattern = schEl('sch', 'pattern')
        pattern.set('abstract', 'true')
        pattern.set('id', 'CardinalityCheck')

        title = schSubEl(pattern, 'sch', 'title')
        title.text = "geonet:replacePlaceholders($loc/strings/cardinality.title, ('#context', '#element'), ('$context', '$element'))"

        rule = schSubEl(pattern, 'sch', 'rule')
        rule.set('context', '$context')

        assertEl = schSubEl(rule, 'sch', 'assert')
        assertEl.set('test', "count($element) >= $min and ('$max' = 'n' or count($element) <= $max)")
        valueOfAssert = schSubEl(assertEl, 'sch', 'value-of')
        valueOfAssert.set(
            'select',
            "geonet:replacePlaceholders($loc/strings/cardinality.assert, ('#context', '#element', '#min', '#max', '#nodecount'), ('$context', '$element', '$min', '$max', string(count($element))))"
        )

        reportEl = schSubEl(rule, 'sch', 'report')
        reportEl.set('test', "count($element) >= $min and ('$max' = 'n' or count($element) <= $max)")
        valueOfReport = schSubEl(reportEl, 'sch', 'value-of')
        valueOfReport.set(
            'select',
            "geonet:replacePlaceholders($loc/strings/cardinality.report, ('#context', '#element', '#min', '#max', '#nodecount'), ('$context', '$element', '$min', '$max', string(count($element))))"
        )

        return pattern

