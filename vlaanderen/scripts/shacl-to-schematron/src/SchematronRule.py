import logging
import json

from constants import classAliases, expressions, omitRules, primaryLanguage
from utilities import addLet, getFullName, getLanguageValue, getLanguageValues, normalizeExpandedNode, safeRemove, schEl, schSubEl, swapURI, castArray


class SchematronRule:

    def __init__(self, prop, targetClass, withProfile):
        self.prop = prop
        self.targetClass = castArray(targetClass)  # always a list
        self.withProfile = withProfile

    def isCardinalityRule(self):
        return 'sh:minCount' in self.prop or 'sh:maxCount' in self.prop

    def getCardinalityPatternElement(self):
        if not self.isCardinalityRule() or self.prop.get('@id') in omitRules:
            return None

        pattern = schEl('sch', 'pattern')
        pattern.set('is-a', self._getCardinalityPatternType())
        pattern.set('id', self._getCardinalityPatternId())

        context = self._getParentContext()
        element = getFullName(self.prop['sh:path'], 'sh:path')
        min_count = str(self.prop.get('sh:minCount', '0'))
        max_count = str(self.prop.get('sh:maxCount', 'n'))

        for name, value in [
            ('context', context),
            ('element', element),
            ('min', min_count),
            ('max', max_count)
        ]:
            param = schSubEl(pattern, 'sch', 'param')
            param.set('name', name)
            param.set('value', value)

        return pattern

    def _getCardinalityPatternType(self):
        return 'MultilingualCardinalityCheck' if self._isLangStringDatatype() else 'CardinalityCheck'

    def _isLangStringDatatype(self):
        datatype = self.prop.get('sh:datatype')
        if datatype is None:
            return False

        for candidate in castArray(datatype):
            if not isinstance(candidate, str):
                continue
            try:
                if getFullName(candidate, 'sh:datatype') == 'rdf:langString':
                    return True
            except Exception:
                continue

        return False

    def getPatternElement(self):
        rule = self._defineRule()
        if rule is not None:
            pattern = schEl('sch', 'pattern')
            patternName = getLanguageValue(self.prop, 'sh:name')
            pattern.set('name', patternName)
            pattern.set('id', self.prop['@id'])

            title = schSubEl(pattern, 'sch', 'title')
            baseTitle = self._getPatternTitle(patternName)
            if 'vl:rule' in self.prop and self.prop['vl:rule'] != '':
                title.text = self.prop['vl:rule'] + '. ' + baseTitle
            else:
                title.text = baseTitle

            if 'rdfs:seeAlso' in self.prop:
                title.text += ' (' + self.prop['rdfs:seeAlso'] + ')'

            pattern.append(rule)
            return pattern
        else:
            return None

    def _expandTargetClasses(self):
        """Expand dcat:Resource to Dataset|DataService|DatasetSeries, deduplicate."""
        expanded = []
        for c in self.targetClass:
            if c == 'dcat:Resource':
                for ec in ['dcat:Dataset', 'dcat:DataService', 'dcat:DatasetSeries']:
                    if ec not in expanded:
                        expanded.append(ec)
            else:
                if c not in expanded:
                    expanded.append(c)
                for alias in classAliases.get(c, []):
                    if alias not in expanded:
                        expanded.append(alias)
        return expanded

    def _getParentContext(self):
        classes = self._expandTargetClasses()
        # suffix = '[$profile]' if self.withProfile else ''
        suffix = ''
        return '|'.join('//' + c + suffix for c in classes)

    def _getContext(self):
        fullname = getFullName(self.prop['sh:path'], 'sh:path')
        classes = self._expandTargetClasses()
        # prop_part = fullname + ('[$profile]' if self.withProfile else '')
        prop_part = fullname
        return '|'.join('//{0}/{1}'.format(c, prop_part) for c in classes)

    def _getCleanContext(self):
        fullname = getFullName(self.prop['sh:path'], 'sh:path')
        classes = self._expandTargetClasses()
        return '|'.join('//{0}/{1}'.format(c, fullname) for c in classes)

    def _defineRule(self):
        try:
            rule = schEl('sch', 'rule')
            fullname = getFullName(self.prop['sh:path'], 'sh:path')
            nodeKind = self._normalizeNodeKind(self.prop.get('sh:nodeKind'))

            if self.prop['@id'] in omitRules:
                return None

            # Collect all assertion conditions for this property
            assertions = []
            context_set = False

            # Handle non-cardinality constraints. Cardinalities are generated in dedicated files.
            if 'sh:class' in self.prop:
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                className = getFullName(self.prop['sh:class'], 'sh:class')
                addLet(rule, 'resource', '@rdf:resource')
                addLet(rule, 'validClass', self._buildClassValidationExpression(className, fullname, '$resource'))
                assertions.append('validClass')

            if 'sh:uniqueLang' in self.prop and self._isTruthyConstraint(self.prop['sh:uniqueLang']):
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                target = getFullName(self.prop['sh:path'], 'sh:path')
                addLet(rule, 'current', '.')
                addLet(rule, 'isUniqueLang', 'count(preceding-sibling::{0}[string() = string($current) and @xml:lang = $current/@xml:lang]) = 0'.format(target))
                assertions.append('isUniqueLang')

            if 'sh:datatype' in self.prop and getFullName(self.prop['sh:datatype'], 'sh:datatype') in ['rdfs:Literal', 'xs:string']:
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                addLet(rule, 'isLiteral', 'normalize-space(.) != \'\'')
                assertions.append('isLiteral')

            elif 'sh:datatype' in self.prop and getFullName(self.prop['sh:datatype'], 'sh:datatype') == 'rdf:langString':
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                addLet(rule, 'isLiteral', 'normalize-space(.) != \'\'')
                addLet(rule, 'hasLang', 'normalize-space(@xml:lang) != \'\'')
                assertions.append(['isLiteral', 'hasLang'])

            elif 'sh:datatype' in self.prop and getFullName(self.prop['sh:datatype'], 'sh:datatype') == 'xs:anyURI':
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                addLet(rule, 'isNotEmpty', 'normalize-space(@rdf:resource) != \'\'')
                addLet(rule, 'isURI', 'matches(@rdf:resource, {0})'.format(expressions['uri']))
                assertions.append(['isNotEmpty', 'isURI'])

            elif 'sh:datatype' in self.prop and getFullName(self.prop['sh:datatype'], 'sh:datatype') in ['xs:dateTime', 'xs:date']:
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                addLet(rule, 'isNotEmpty', 'normalize-space(.) != \'\'')
                addLet(rule, 'isDate', 'matches(., {0})'.format(expressions['dateAndDateTime']))
                assertions.append(['isNotEmpty', 'isDate'])

            if self._hasConceptSchemeNodeRestriction():
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                localProp = self._getNodePropertyRestriction()
                value = swapURI(localProp['sh:hasValue'])
                addLet(rule, 'hasValue', "skos:Concept/skos:inScheme/@rdf:resource = '{0}'".format(value))
                assertions.append('hasValue')

            elif 'sh:hasValue' in self.prop:
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                addLet(rule, 'hasValue', "string() = '{0}' or */@rdf:about = '{0}' or ./@rdf:resource = '{0}'".format(self.prop['sh:hasValue']))
                assertions.append('hasValue')

            if 'sh:or' in self.prop:
                alternatives = self._getOrAlternatives()
                iriPatterns = [
                    alt['sh:pattern'] for alt in alternatives
                    if self._normalizeNodeKind(alt.get('sh:nodeKind')) == 'sh:IRI' and 'sh:pattern' in alt
                ]
                classAlternatives = [
                    getFullName(alt['sh:class'], 'sh:or/sh:class') for alt in alternatives if 'sh:class' in alt
                ]
                if len(iriPatterns) > 0 or len(classAlternatives) > 0:
                    if not context_set:
                        rule.set('context', self._getContext())
                        context_set = True
                    addLet(rule, 'resource', '(@rdf:resource, */@rdf:about)[1]')
                    alternativeChecks = []

                    if len(iriPatterns) > 0:
                        iriPatternExpr = self._buildOrPatternExpression(iriPatterns)
                        alternativeChecks.append('(matches($resource, {0}) and {1})'.format(expressions['uri'], iriPatternExpr))

                    if len(classAlternatives) > 0:
                        classChecks = [
                            self._buildClassValidationExpression(className, fullname, '$resource') for className in classAlternatives
                        ]
                        alternativeChecks.append('({0})'.format(' or '.join(classChecks)))

                    addLet(rule, 'matchesOrAlternative', '({0})'.format(' or '.join(alternativeChecks)))
                    assertions.append('matchesOrAlternative')
                else:
                    self._logMissingRuleConversion()

            if 'sh:pattern' in self.prop:
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                patternValue = self.prop['sh:pattern']
                if nodeKind == 'sh:IRI':
                    addLet(rule, 'resource', '(@rdf:resource, */@rdf:about)[1]')
                    addLet(rule, 'isIRI', 'matches($resource, {0})'.format(expressions['uri']))
                    addLet(rule, 'matchesPattern', "matches($resource, '{0}')".format(patternValue))
                    assertions.append(['isIRI', 'matchesPattern'])
                else:
                    addLet(rule, 'matchesPattern', "matches(normalize-space(.), '{0}')".format(patternValue))
                    assertions.append('matchesPattern')

            # sh:nodeKind constraints - these can be combined with cardinality
            if nodeKind == 'sh:IRI':
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                addLet(rule, 'resource', '(@rdf:resource, */@rdf:about)[1]')
                addLet(rule, 'isIRI', 'matches($resource, {0})'.format(expressions['uri']))
                if fullname == 'foaf:mbox':
                    addLet(rule, 'isMailto', "starts-with(lower-case($resource), 'mailto:')")
                    assertions.append(['isIRI', 'isMailto'])
                else:
                    assertions.append('isIRI')

            elif nodeKind == 'sh:IRIOrLiteral':
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                addLet(rule, 'resource', '(@rdf:resource, */@rdf:about)[1]')
                addLet(rule, 'isIRI', 'matches($resource, {0})'.format(expressions['uri']))
                assertions.append('isIRI')

            elif nodeKind == 'sh:Literal':
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                addLet(rule, 'isLiteral', "normalize-space(.) != ''")
                assertions.append('isLiteral')

            elif nodeKind == 'sh:BlankNodeOrIRI':
                if not context_set:
                    rule.set('context', self._getContext())
                    context_set = True
                addLet(rule, 'resource', '(@rdf:resource, */@rdf:about)[1]')
                addLet(rule, 'isIRI', 'matches($resource, {0})'.format(expressions['uri']))
                addLet(rule, 'isBlankNode', 'count(@rdf:resource) = 0 and count(@rdf:about) = 0 and count(*[not(starts-with(name(), \'geonet:\'))]) >= 1')
                addLet(rule, 'isBlankNodeOrIRI', '$isIRI or $isBlankNode')
                assertions.append('isBlankNodeOrIRI')

            # If no assertions were collected or no context was set, handle accordingly
            if not assertions:
                if self.isCardinalityRule():
                    return None
                self._logMissingRuleConversion()
                return None

            # Apply all collected assertions to the rule
            # Flatten assertions list: some items may be lists themselves
            flattened_assertions = []
            for assertion in assertions:
                if isinstance(assertion, list):
                    flattened_assertions.extend(assertion)
                else:
                    flattened_assertions.append(assertion)
            self._defineReport(flattened_assertions, rule)
            return rule
        except Exception as err:
            raise RuntimeError(
                'Error converting SHACL rule: id={0}, path={1}, targetClass={2}, keys={3}.'.format(
                    self.prop.get('@id', '<unknown>'),
                    self.prop.get('sh:path', '<missing>'),
                    self.targetClass,
                    sorted(self.prop.keys())
                )
            ) from err

    def _defineReport(self, varNames, rule):
        messageTranslations = self._getMessageTranslations()
        messageDescription = self._getMessageText(messageTranslations)
        pathText = getFullName(self.prop['sh:path'], 'sh:path')
        message = '{0} ({1})'.format(messageDescription, pathText)
        varNames = castArray(varNames)
        test = ' and '.join(map(lambda varName: '$' + varName, varNames))

        localizedMessages = {
            lang: '{0} ({1})'.format(text, pathText)
            for lang, text in messageTranslations.items()
            if isinstance(text, str) and text.strip() != ''
        }

        assertEl = schSubEl(rule, 'sch', 'assert')
        assertEl.set('test', test)
        assertEl.set('data-localized-texts', json.dumps(localizedMessages, ensure_ascii=False, sort_keys=True))
        assertEl.text = message
        reportEl = schSubEl(rule, 'sch', 'report')
        reportEl.set('test', test)
        reportEl.set('data-localized-texts', json.dumps(localizedMessages, ensure_ascii=False, sort_keys=True))
        reportEl.text = message

    def _getMessageText(self, messageTranslations=None):
        messageTranslations = self._getMessageTranslations() if messageTranslations is None else messageTranslations
        if 'en' in messageTranslations and messageTranslations['en'].strip() != '':
            return messageTranslations['en']

        return getLanguageValue(messageTranslations, preferredLanguage='en', fallbackLangs=['en'], default=self._getDefaultMessageText()).strip()

    def _getMessageTranslations(self):
        vlMessage = self.prop['vl:message'] if 'vl:message' in self.prop else None
        messageSource = vlMessage if vlMessage else self.prop['sh:message'] if 'sh:message' in self.prop else self.prop.get('sh:description')
        messageTranslations = getLanguageValues(messageSource)
        defaultMessage = self._getDefaultMessageText()

        if 'en' not in messageTranslations or messageTranslations['en'].strip() == '':
            messageTranslations['en'] = defaultMessage

        return messageTranslations


    def _getPatternTitle(self, patternName):
        description = getLanguageValue(self.prop, 'sh:description', default='').strip()
        patternName = (patternName or '').strip()

        if patternName != '' and description != '':
            return '{0} - {1}'.format(patternName.capitalize(), description)
        if patternName != '':
            return patternName.capitalize()
        if description != '':
            return description
        return self._getDefaultPatternTitle()

    def _getDefaultPatternTitle(self):
        element = self._formatConstraintValue(self.prop.get('sh:path'), 'sh:path')
        return '{0} - {1}'.format(element, self._getRuleKindLabel())

    def _getRuleKindLabel(self):
        if 'sh:class' in self.prop:
            return 'class {0}'.format(self._formatConstraintValue(self.prop['sh:class'], 'sh:class'))

        if 'sh:uniqueLang' in self.prop and self.prop['sh:uniqueLang'] == 'true':
            return 'unique language constraint'

        if 'sh:datatype' in self.prop:
            return 'datatype {0}'.format(self._formatConstraintValue(self.prop['sh:datatype'], 'sh:datatype'))

        if self._hasConceptSchemeNodeRestriction():
            localProp = self._getNodePropertyRestriction()
            return 'concept scheme {0}'.format(self._formatConstraintValue(localProp.get('sh:hasValue', 'required value')))

        if 'sh:hasValue' in self.prop:
            return 'fixed value {0}'.format(self._formatConstraintValue(self.prop['sh:hasValue']))

        if 'sh:or' in self.prop:
            return 'alternative constraint'

        if 'sh:pattern' in self.prop:
            return 'IRI pattern' if self.prop.get('sh:nodeKind') == 'sh:IRI' else 'pattern'

        if self.prop.get('sh:nodeKind') == 'sh:IRI':
            return 'IRI constraint'

        if self.prop.get('sh:nodeKind') == 'sh:IRIOrLiteral':
            return 'IRI or literal constraint'

        if self.prop.get('sh:nodeKind') == 'sh:BlankNodeOrIRI':
          return 'BlankNode or IRI constraint'

        if self.prop.get('sh:nodeKind') == 'sh:Literal':
            return 'literal constraint'

        if 'sh:minCount' in self.prop and 'sh:maxCount' in self.prop:
            return 'cardinality between {0} and {1}'.format(self.prop['sh:minCount'], self.prop['sh:maxCount'])

        if 'sh:minCount' in self.prop:
            return 'minimum cardinality {0}'.format(self.prop['sh:minCount'])

        if 'sh:maxCount' in self.prop:
            return 'maximum cardinality {0}'.format(self.prop['sh:maxCount'])

        return 'constraint'

    def _getDefaultMessageText(self):
        if 'sh:class' in self.prop:
            return 'Referenced resource must be of type {0}'.format(self._formatConstraintValue(self.prop['sh:class'], 'sh:class'))

        if 'sh:uniqueLang' in self.prop and self.prop['sh:uniqueLang'] == 'true':
            return 'Values must not reuse the same language tag'

        if 'sh:datatype' in self.prop:
            datatype = self._formatConstraintValue(self.prop['sh:datatype'], 'sh:datatype')
            if datatype in ['rdfs:Literal', 'xs:string']:
                return 'Value must be a non-empty literal'
            if datatype == 'rdf:langString':
                return 'Value must be a non-empty language-tagged literal'
            if datatype == 'xs:anyURI':
                return 'Value must be a non-empty URI'
            if datatype in ['xs:dateTime', 'xs:date']:
                return 'Value must be a valid {0}'.format(datatype)
            return 'Value must match datatype {0}'.format(datatype)

        if self._hasConceptSchemeNodeRestriction():
            localProp = self._getNodePropertyRestriction()
            return 'Value must belong to concept scheme {0}'.format(localProp.get('sh:hasValue', 'the required scheme'))

        if 'sh:hasValue' in self.prop:
            return 'Value must be {0}'.format(self.prop['sh:hasValue'])

        if 'sh:or' in self.prop:
            return 'Value must satisfy at least one of the allowed alternatives'

        if 'sh:pattern' in self.prop:
            if self.prop.get('sh:nodeKind') == 'sh:IRI':
                return 'IRI must match the required pattern'
            return 'Value must match the required pattern'

        if self.prop.get('sh:nodeKind') == 'sh:IRI':
            return 'Value must be a mailto IRI' if self._formatConstraintValue(self.prop.get('sh:path'), 'sh:path') == 'foaf:mbox' else 'Value must be an IRI'

        if self.prop.get('sh:nodeKind') == 'sh:IRIOrLiteral':
            return 'Value must be an IRI or a literal'

        if self.prop.get('sh:nodeKind') == 'sh:Literal':
            return 'Value must be a literal'

        if 'sh:minCount' in self.prop and 'sh:maxCount' in self.prop:
            return 'Cardinality must be between {0} and {1}'.format(self.prop['sh:minCount'], self.prop['sh:maxCount'])

        if 'sh:minCount' in self.prop:
            return 'At least {0} value(s) are required'.format(self.prop['sh:minCount'])

        if 'sh:maxCount' in self.prop:
            return 'At most {0} value(s) are allowed'.format(self.prop['sh:maxCount'])

        return 'Value does not satisfy the SHACL constraint'

    def _isTruthyConstraint(self, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ['true', '1']
        return bool(value)

    def _normalizeNodeKind(self, value):
        if not isinstance(value, str):
            return value
        if value.startswith('shacl:'):
            return 'sh:' + value.split(':', 1)[1]
        return value

    def _formatConstraintValue(self, value, source=None):
        if isinstance(value, str):
            try:
                return getFullName(value, source) if (':/' in value or value.startswith('http://') or value.startswith('https://') or value.startswith('_:')) else value
            except Exception:
                return value
        return str(value)

    def _hasConceptSchemeNodeRestriction(self):
        node_property = self._getNodePropertyRestriction()
        return isinstance(node_property, dict) and node_property.get('sh:class') == 'skos:ConceptScheme' and 'sh:hasValue' in node_property

    def _getOrAlternatives(self):
        alternatives = castArray(self.prop.get('sh:or', []))
        if len(alternatives) == 1 and isinstance(alternatives[0], dict) and '@list' in alternatives[0]:
            alternatives = castArray(alternatives[0]['@list'])

        normalized = []
        for alt in alternatives:
            if isinstance(alt, list):
                for nested in alt:
                    if isinstance(nested, dict):
                        normalized.append(normalizeExpandedNode(nested))
                continue
            if isinstance(alt, dict):
                normalized.append(normalizeExpandedNode(alt))
        return normalized

    def _buildOrPatternExpression(self, patterns):
        checks = ["matches($resource, '{0}')".format(pattern) for pattern in patterns]
        return '({0})'.format(' or '.join(checks))

    def _buildClassValidationExpression(self, className, fullname, resourceVar):
        if fullname == 'vcard:hasEmail':
            return 'matches({0}, {1})'.format(resourceVar, expressions['email'])

        if className == 'dcat:DataService' or className == 'dcat:Dataset' or className == 'rdfs:Resource':
            return 'matches({0}, {1})'.format(resourceVar, expressions['uri'])

        classCandidates = [className]
        for alias in classAliases.get(className, []):
            if alias not in classCandidates:
                classCandidates.append(alias)

        if className == 'dcat:Resource':
            localXpath = 'dcat:Dataset|dcat:DataService|dcat:DatasetSeries'
            globalXpath = '(//dcat:Dataset|//dcat:DataService|//dcat:DatasetSeries)'
        elif len(classCandidates) == 1:
            localXpath = classCandidates[0]
            globalXpath = '//' + classCandidates[0]
        else:
            localXpath = '|'.join(classCandidates)
            globalXpath = '(//{0})'.format('|//'.join(classCandidates))

        return 'count({0}) = 1 or count({1}[@rdf:about = {2}]) = 1'.format(localXpath, globalXpath, resourceVar)

    def _getCardinalityPatternId(self):
        classes = self._expandTargetClasses()
        class_part = '_'.join(self._sanitizePatternIdPart(c) for c in classes)
        element_part = self._sanitizePatternIdPart(getFullName(self.prop['sh:path'], 'sh:path'))
        rule_part = self._sanitizePatternIdPart(self.prop.get('@id', 'rule'))
        return '{0}_{1}_{2}'.format(class_part, element_part, rule_part)

    def _sanitizePatternIdPart(self, value):
        return ''.join(ch if ch.isalnum() else '_' for ch in value).strip('_')

    def _getNodePropertyRestriction(self):
        node = self.prop.get('sh:node')
        if isinstance(node, list):
            node = node[0] if len(node) > 0 else None
        if not isinstance(node, dict):
            return None

        node_property = node.get('sh:property')
        if isinstance(node_property, list):
            node_property = node_property[0] if len(node_property) > 0 else None
        return node_property if isinstance(node_property, dict) else None

    def _logMissingRuleConversion(self):
        keys = list(self.prop.keys())
        safeRemove(keys, '@id')
        safeRemove(keys, 'rdfs:seeAlso')
        safeRemove(keys, 'sh:description')
        safeRemove(keys, 'sh:name')
        safeRemove(keys, 'vl:message')
        safeRemove(keys, 'sh:severity')
        safeRemove(keys, 'vl:rule')
        safeRemove(keys, 'vlb:rule')
        details = ', '.join(map(lambda key: key + '=' + self._stringifyLogValue(self.prop[key]), keys))
        logging.error(
            'The property with id ' +
            self.prop['@id'] +
            ' could not be converted to schematron: ' +
            details + '. Add support for this type of SHACL rule.'
        )

    def _stringifyLogValue(self, value):
        if isinstance(value, str):
            return value
        try:
            return json.dumps(value, ensure_ascii=False, sort_keys=True)
        except TypeError:
            return str(value)

