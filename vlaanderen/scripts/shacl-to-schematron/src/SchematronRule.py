import logging

from constants import expressions, omitRules
from utilities import addLet, getFullName, safeRemove, schEl, schSubEl, swapURI, castArray


class SchematronRule:

    def __init__(self, prop, targetClass, withProfile):
        self.prop = prop
        self.targetClass = targetClass
        self.withProfile = withProfile

    def getPatternElement(self):
        rule = self._defineRule() if self.targetClass != 'dcat:Catalog' else None
        if rule is not None:
            pattern = schEl('sch', 'pattern')
            pattern.set('name', self.prop['sh:name']['nl'])
            pattern.set('id', self.prop['@id'])

            title = schSubEl(pattern, 'sch', 'title')
            baseTitle = '{0} - {1}'.format(self.prop['sh:name']['nl'].capitalize(), self.prop['sh:description']['nl'])
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
        rule = schEl('sch', 'rule')
        fullname = getFullName(self.prop['sh:path'])

        if self.prop['@id'] in omitRules:
            return None

        if 'sh:maxCount' in self.prop:
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

        elif 'sh:node' in self.prop and self.prop['sh:node']['sh:property']['sh:class'] == 'skos:ConceptScheme':
            rule.set('context', self._getContext())
            localProp = self.prop['sh:node']['sh:property']
            value = swapURI(localProp['sh:hasValue'])
            addLet(rule, 'hasValue', "skos:Concept/skos:inScheme/@rdf:resource = '{0}'".format(value))
            self._defineReport('hasValue', rule)

        elif 'sh:hasValue' in self.prop:
            rule.set('context', self._getContext())
            addLet(rule, 'hasValue', "string() = '{0}' or */@rdf:about = '{0}' or ./@rdf:resource = '{0}'".format(self.prop['sh:hasValue']))
            self._defineReport('hasValue', rule)

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

    def _defineReport(self, varNames, rule):
        message = '{0} ({1})'.format(self.prop['vl:message']['nl'], getFullName(self.prop['sh:path']))
        varNames = castArray(varNames)
        test = ' and '.join(map(lambda varName: '$' + varName, varNames))
        assertEl = schSubEl(rule, 'sch', 'assert')
        assertEl.set('test', test)
        assertEl.text = message
        reportEl = schSubEl(rule, 'sch', 'report')
        reportEl.set('test', test)
        reportEl.text = message

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
        logging.error(
            'The property with id ' +
            self.prop['@id'] +
            ' could not be converted to schematron: ' +
            ', '.join(map(lambda key: key + '=' + self.prop[key], keys))
        )
