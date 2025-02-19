import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from os.path import isfile

from constants import dcatNamespaces, locOutput, schOutput, schNamespaces
from utilities import addLet, writeXmlToFile, schEl, schSubEl


class SchematronGenerator:

    def __init__(self, name, title, profile=None):
        if len(name) >= 40:
            logging.error('Schematron file name "{0}" too long, must not be above 40 characters'.format(name))
            exit(1)

        self.name = name
        self.title = title
        self.profile = profile
        self.rules = self._getDefaultRules()

    def addRule(self, rule):
        rulePattern = rule.getPatternElement()
        if rulePattern is not None:
            self.rules.append(rulePattern)

    def generateSchematron(self):
        root = schEl('sch', 'schema')
        title = schSubEl(root, 'sch', 'title')
        title.set('xmlns', 'http://www.w3.org/2001/XMLSchema')
        title.text = '{$loc/strings/schematron.title}'

        for dcatNs in dcatNamespaces:
            nsEl = schSubEl(root, 'sch', 'ns')
            nsEl.set('prefix', dcatNs)
            nsEl.set('uri', dcatNamespaces[dcatNs])

        if self.profile is not None:
            addLet(root, 'profile', 'boolean(/*[starts-with(//dcat:CatalogRecord//dct:Standard/@rdf:about, \'{0}\')])'.format(self.profile))

        for rule in self.rules:
            root.append(rule)

        Path(schOutput).mkdir(parents=True, exist_ok=True)
        writeXmlToFile(root, Path(schOutput + '/' + self.name + '.sch').resolve())

    def generateLocFiles(self):
        for loc in self.title:
            Path(locOutput + '/' + loc).mkdir(parents=True, exist_ok=True)
            root = ET.Element('strings')
            locTitle = ET.SubElement(root, 'schematron.title')
            locTitle.text = self.title[loc]
            writeXmlToFile(root, Path(locOutput + '/' + loc + '/' + self.name + '.xml').resolve())

    def _getDefaultRules(self):
        filename = Path('custom_rules/' + self.name + '.sch').resolve()
        return ET.parse(filename).findall('sch:pattern', schNamespaces) if isfile(filename) else []
