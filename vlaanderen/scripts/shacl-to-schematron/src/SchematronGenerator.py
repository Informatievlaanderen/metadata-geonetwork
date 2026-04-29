import logging
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from os.path import isfile

from constants import dcatNamespaces, locOutput, schOutput, schNamespaces
from utilities import addLet, writeXmlToFile, schEl, schSubEl, translateText


class SchematronGenerator:

    def __init__(self, name, title, profile=None, includeCardinalityAbstract=False, schematronTitle=None, condition=None, enableTranslation=False, primaryLanguage='en'):
        self.name = name
        self.title = title
        self.profile = profile
        self.condition = condition
        self.enableTranslation = enableTranslation
        self.primaryLanguage = primaryLanguage
        self.includeCardinalityAbstract = includeCardinalityAbstract
        self.schematronTitle = schematronTitle if schematronTitle is not None else self._getSchematronTitle(title)
        self.locKeyPrefix = self._getLocKeyPrefix()
        self.rules = self._getDefaultRules()
        if self.includeCardinalityAbstract:
            self.rules.append(self._buildCardinalityAbstractPattern())
            self.rules.append(self._buildMultilingualCardinalityAbstractPattern())
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

        if self.profile is not None or self.condition is not None:
            addLet(root, 'profile', self.condition if self.condition else 'true()')

        for rule in self.rules:
            root.append(rule)

        self._externalizeRuleText(root)

        Path(schOutput).mkdir(parents=True, exist_ok=True)
        writeXmlToFile(root, Path(schOutput + '/' + self.name + '.sch').resolve())

    def generateLocFiles(self):
        _langMap = {'dut': 'nl', 'eng': 'en', 'fre': 'fr', 'ger': 'de'}

        if not self.enableTranslation:
            logging.debug('Translation disabled by configuration; localization files will use source text for all locales.')

        for loc in self.title:
            Path(locOutput + '/' + loc).mkdir(parents=True, exist_ok=True)
            root = ET.Element('strings')
            locTitle = ET.SubElement(root, 'schematron.title')
            locTitle.text = self.schematronTitle[loc]

            lang_code = _langMap.get(loc, loc)
            primary_lang = _langMap.get(self.primaryLanguage, self.primaryLanguage)

            for key in sorted(self.locEntries.keys()):
                locEl = ET.SubElement(root, key)
                text = self.locEntries[key]

                # Translate if target language differs from primary
                if self.enableTranslation and lang_code != primary_lang:
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
            # Keys may be provided by schematron-shared.xml in deployed environments.
        }

    def _getSchematronTitle(self, defaultTitle):
        if not self.includeCardinalityAbstract:
            return defaultTitle

        suffixes = {
            'dut': 'Kardinaliteiten',
            'eng': 'Cardinalities',
            'fre': 'Cardinalités',
            'ger': 'Kardinalitäten'
        }

        cardinalityTitle = {}
        for loc, title in defaultTitle.items():
            suffix = suffixes.get(loc, 'Cardinalities')
            if ' - ' not in title:
                cardinalityTitle[loc] = '{0} - {1}'.format(title, suffix)
                continue

            baseTitle, titleQualifier = title.split(' - ', 1)
            qualifierMatch = re.match(r'^(.*?)(\s*\([^)]*\))?$', titleQualifier)
            qualifierSuffix = qualifierMatch.group(2) if qualifierMatch is not None and qualifierMatch.group(2) is not None else ''
            cardinalityTitle[loc] = '{0} - {1}{2}'.format(baseTitle, suffix, qualifierSuffix)

        return cardinalityTitle

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

    def _buildMultilingualCardinalityAbstractPattern(self):
        pattern = schEl('sch', 'pattern')
        pattern.set('abstract', 'true')
        pattern.set('id', 'MultilingualCardinalityCheck')

        title = schSubEl(pattern, 'sch', 'title')
        title.text = "geonet:replacePlaceholders($loc/strings/multilingual.cardinality.title, ('#context', '#element'), ('$context', '$element'))"

        rule = schSubEl(pattern, 'sch', 'rule')
        rule.set('context', '$context')

        testExpr = (
            "(count($element[@xml:lang]) = 0 or count($element[not(@xml:lang)]) = 0) and "
            "((count(distinct-values($element/@xml:lang)) = count($element[@xml:lang])) or '$max' = 'n') and "
            "((count($element[not(@xml:lang)]) <= 1) or '$max' = 'n') and "
            "(count(distinct-values($element/@xml:lang)) >= $min or (count($element[not(@xml:lang)]) >= $min))"
        )

        assertEl = schSubEl(rule, 'sch', 'assert')
        assertEl.set('test', testExpr)
        valueOfAssert = schSubEl(assertEl, 'sch', 'value-of')
        valueOfAssert.set(
            'select',
            "geonet:replacePlaceholders($loc/strings/multilingual.cardinality.assert, ('#min'), ('$min'))"
        )

        reportEl = schSubEl(rule, 'sch', 'report')
        reportEl.set('test', testExpr)
        valueOfReport = schSubEl(reportEl, 'sch', 'value-of')
        valueOfReport.set(
            'select',
            "geonet:replacePlaceholders($loc/strings/multilingual.cardinality.report, ('#min'), ('$min'))"
        )

        return pattern

