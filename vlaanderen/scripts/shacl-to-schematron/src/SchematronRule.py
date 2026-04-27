import logging
import json

from constants import expressions, omitRules
from utilities import addLet, getFullName, getLanguageValue, normalizeExpandedNode, safeRemove, schEl, schSubEl, swapURI, castArray


class SchematronRule:

    def __init__(self, prop, targetClass, withProfile):
        self.prop = prop
        self.targetClass = targetClass
        self.withProfile = withProfile

    def getPatternElement(self):
        rule = self._defineRule() if self.targetClass != 'dcat:Catalog' else None
        if rule is not None:
            pattern = schEl('sch', 'pattern')
            patternName = getLanguageValue(self.prop, 'sh:name')
            pattern.set('name', patternName)
            pattern.set('id', self.prop['@id'])

            title = schSubEl(pattern, 'sch', 'title')
            description = getLanguageValue(self.prop, 'sh:description')
            baseTitle = '{0} - {1}'.format(patternName.capitalize(), description)
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

    def _getParentContext(self):
        if self.targetClass == 'dcat:Resource':
            return '//dcat:Dataset|//dcat:DataService' if not self.withProfile else '//dcat:Dataset[$profile]|//dcat:DataService[$profile]'
        else:
            context = '//' + self.targetClass
            return context if not self.withProfile else context + '[$profile]'

    def _getContext(self):
        fullname = getFullName(self.prop['sh:path'])
        if self.withProfile:
            fullname += '[$profile]'
        if self.targetClass == 'dcat:Resource':
            return '//dcat:Dataset/{0}|//dcat:DataService/{0}'.format(fullname)
        else:
            return '//{0}/{1}'.format(self.targetClass, fullname)

    def _getCleanContext(self):
        return '//{0}/{1}'.format(self.targetClass, getFullName(self.prop['sh:path']))

    def _defineRule(self):
        try:
            rule = schEl('sch', 'rule')
            fullname = getFullName(self.prop['sh:path'])

            if self.prop['@id'] in omitRules:
                return None

            if 'sh:minCount' in self.prop and 'sh:maxCount' in self.prop:
                rule.set('context', self._getParentContext())
                addLet(rule, 'validMin', 'count({0}) >= {1}'.format(fullname, self.prop['sh:minCount']))
                addLet(rule, 'validMax', 'count({0}) <= {1}'.format(fullname, self.prop['sh:maxCount']))
                self._defineReport(['validMin', 'validMax'], rule)

            elif 'sh:maxCount' in self.prop:
                rule.set('context', self._getParentContext())
                addLet(rule, 'validMax', 'count({0}) <= {1}'.format(fullname, self.prop['sh:maxCount']))
                self._defineReport('validMax', rule)

            elif 'sh:minCount' in self.prop:
                rule.set('context', self._getParentContext())
                addLet(rule, 'validMin', 'count({0}) >= {1}'.format(fullname, self.prop['sh:minCount']))
                self._defineReport('validMin', rule)

            elif 'sh:class' in self.prop:
                rule.set('context', self._getContext())
                className = getFullName(self.prop['sh:class'])
                localXpath = className if className != 'dcat:Resource' else 'dcat:Dataset|dcat:DataService'
                globalXpath = '//' + className if className != 'dcat:Resource' else '(//dcat:Dataset|//dcat:DataService)'
                addLet(rule, 'resource', '@rdf:resource')
                if className == 'dcat:DataService' or className == 'dcat:Dataset' or className == 'rdfs:Resource':
                    addLet(rule, 'validClass', 'matches($resource, {0})'.format(expressions['uri']))
                else:
                    addLet(rule, 'validClass', 'count({0}) = 1 or count({1}[@rdf:about = $resource]) = 1'.format(localXpath, globalXpath))
                self._defineReport('validClass', rule)

            elif 'sh:uniqueLang' in self.prop and self.prop['sh:uniqueLang'] == 'true':
                rule.set('context', self._getContext())
                target = getFullName(self.prop['sh:path'])
                addLet(rule, 'current', '.')
                addLet(rule, 'isUniqueLang', 'count(preceding-sibling::{0}[string() = string($current) and @xml:lang = $current/@xml:lang]) = 0'.format(target))
                self._defineReport('isUniqueLang', rule)

            elif 'sh:datatype' in self.prop and getFullName(self.prop['sh:datatype']) in ['rdfs:Literal', 'xs:string']:
                rule.set('context', self._getContext())
                addLet(rule, 'isLiteral', 'normalize-space(.) != \'\'')
                self._defineReport('isLiteral', rule)

            elif 'sh:datatype' in self.prop and getFullName(self.prop['sh:datatype']) == 'rdf:langString':
                rule.set('context', self._getContext())
                addLet(rule, 'isLiteral', 'normalize-space(.) != \'\'')
                addLet(rule, 'hasLang', 'normalize-space(@xml:lang) != \'\'')
                self._defineReport(['isLiteral', 'hasLang'], rule)

            elif 'sh:datatype' in self.prop and getFullName(self.prop['sh:datatype']) == 'xs:anyURI':
                rule.set('context', self._getContext())
                addLet(rule, 'isNotEmpty', 'normalize-space(@rdf:resource) != \'\'')
                addLet(rule, 'isURI', 'matches(@rdf:resource, {0})'.format(expressions['uri']))
                self._defineReport(['isNotEmpty', 'isURI'], rule)

            elif 'sh:datatype' in self.prop and getFullName(self.prop['sh:datatype']) in ['xs:dateTime', 'xs:date']:
                rule.set('context', self._getContext())
                addLet(rule, 'isNotEmpty', 'normalize-space(.) != \'\'')
                addLet(rule, 'isDate', 'matches(., {0})'.format(expressions['dateAndDateTime']))
                self._defineReport(['isNotEmpty', 'isDate'], rule)

            elif self._hasConceptSchemeNodeRestriction():
                rule.set('context', self._getContext())
                localProp = self._getNodePropertyRestriction()
                value = swapURI(localProp['sh:hasValue'])
                addLet(rule, 'hasValue', "skos:Concept/skos:inScheme/@rdf:resource = '{0}'".format(value))
                self._defineReport('hasValue', rule)

            elif 'sh:hasValue' in self.prop:
                rule.set('context', self._getContext())
                addLet(rule, 'hasValue', "string() = '{0}' or */@rdf:about = '{0}' or ./@rdf:resource = '{0}'".format(self.prop['sh:hasValue']))
                self._defineReport('hasValue', rule)

            elif 'sh:or' in self.prop:
                alternatives = self._getOrAlternatives()
                iriPatterns = [alt['sh:pattern'] for alt in alternatives if alt.get('sh:nodeKind') == 'sh:IRI' and 'sh:pattern' in alt]
                if len(iriPatterns) > 0:
                    rule.set('context', self._getContext())
                    addLet(rule, 'resource', '@rdf:resource')
                    addLet(rule, 'isIRI', 'matches($resource, {0})'.format(expressions['uri']))
                    addLet(rule, 'matchesOrPattern', self._buildOrPatternExpression(iriPatterns))
                    self._defineReport(['isIRI', 'matchesOrPattern'], rule)
                else:
                    self._logMissingRuleConversion()
                    return None

            elif 'sh:pattern' in self.prop:
                rule.set('context', self._getContext())
                patternValue = self.prop['sh:pattern']
                if 'sh:nodeKind' in self.prop and self.prop['sh:nodeKind'] == 'sh:IRI':
                    addLet(rule, 'resource', '@rdf:resource')
                    addLet(rule, 'isIRI', 'matches($resource, {0})'.format(expressions['uri']))
                    addLet(rule, 'matchesPattern', "matches($resource, '{0}')".format(patternValue))
                    self._defineReport(['isIRI', 'matchesPattern'], rule)
                else:
                    addLet(rule, 'matchesPattern', "matches(normalize-space(.), '{0}')".format(patternValue))
                    self._defineReport('matchesPattern', rule)

            elif 'sh:nodeKind' in self.prop and self.prop['sh:nodeKind'] == 'sh:IRI':
                rule.set('context', self._getContext())
                addLet(rule, 'resource', '@rdf:resource')
                addLet(rule, 'isIRI', 'matches($resource, {0})'.format(expressions['uri']))
                if fullname == 'foaf:mbox':
                    addLet(rule, 'isMailto', "starts-with(lower-case($resource), 'mailto:')")
                    self._defineReport(['isIRI', 'isMailto'], rule)
                else:
                    self._defineReport('isIRI', rule)

            elif 'sh:nodeKind' in self.prop and self.prop['sh:nodeKind'] == 'sh:IRIOrLiteral':
                rule.set('context', self._getContext())
                addLet(rule, 'resource', '@rdf:resource')
                addLet(rule, 'isIRI', 'matches($resource, {0})'.format(expressions['uri']))
                self._defineReport('isIRI', rule)

            elif 'sh:nodeKind' in self.prop and self.prop['sh:nodeKind'] == 'sh:Literal':
                rule.set('context', self._getContext())
                addLet(rule, 'isLiteral', "count(@rdf:resource) = 0 and count(@rdf:about) = 0 and count(*[not(starts-with(name(), 'geonet:'))]) = 0")
                self._defineReport('isLiteral', rule)

            elif 'sh:nodeKind' in self.prop and self.prop['sh:nodeKind'] == 'sh:BlankNodeOrIRI':
                # rule.set('context', self._getContext())
                # addLet(rule, 'isBlankNode', 'count(@rdf:resource) = 0')
                # addLet(rule, 'isIRI', 'count(@rdf:resource) = 1 and count(*) < 1')
                # addLet(rule, 'isBlankNodeOrIRI', '$isBlankNode or $isIRI')
                # self._defineReport('isBlankNodeOrIRI', rule)
                return None

            else:
                self._logMissingRuleConversion()
                return None

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
        messageDescription = self._getMessageText()
        message = '{0} ({1})'.format(messageDescription, getFullName(self.prop['sh:path']))
        varNames = castArray(varNames)
        test = ' and '.join(map(lambda varName: '$' + varName, varNames))
        assertEl = schSubEl(rule, 'sch', 'assert')
        assertEl.set('test', test)
        assertEl.text = message
        reportEl = schSubEl(rule, 'sch', 'report')
        reportEl.set('test', test)
        reportEl.text = message

    def _getMessageText(self):
        vlMessage = self.prop['vl:message'] if 'vl:message' in self.prop else None
        messageSource = vlMessage if vlMessage else self.prop['sh:message'] if 'sh:message' in self.prop else self.prop.get('sh:description', '')
        return getLanguageValue(messageSource)

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

