import logging
import xml.etree.ElementTree as ET

from SchematronGenerator import SchematronGenerator
from SchematronRule import SchematronRule
from constants import shaclSpecsConfig, schNamespaces
from utilities import loadJsonUrl, castArray, getFullName


def configureLogger():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)-5s - %(message)s'
    )


def registerNamespaces():
    for ns in schNamespaces:
        ET.register_namespace(ns, schNamespaces[ns])


def generateFromSpec(config):
    schematron = SchematronGenerator(config['name'], config['title'], config['profile'])
    for url in castArray(config['url']):
        spec = loadJsonUrl(url)
        for shape in spec['shapes']:
            for prop in shape['sh:property']:
                if shouldBeAdded(config, prop):
                    schematron.addRule(SchematronRule(
                        prop,
                        getTargetClass(shape),
                        bool(config['profile'])
                    ))
    schematron.generateSchematron()
    schematron.generateLocFiles()


def shouldBeAdded(config, prop):
    return ('level' in config and 'sh:severity' in prop and prop['sh:severity'] == config['level']) or \
        ('level' not in config and 'sh:severity' not in prop)


def getTargetClass(shape):
    targetClass = ''
    if 'sh:targetObjectsOf' not in shape and 'sh:targetClass' not in shape:
        raise "Target class could not be found" + shape
    if 'sh:targetObjectsOf' in shape:
        targetClass += getFullName(shape['sh:targetObjectsOf']) + '/'
    if 'sh:targetClass' in shape:
        targetClass += getFullName(shape['sh:targetClass'])
    else:
        targetClass += '*'

    return targetClass


if __name__ == '__main__':
    configureLogger()
    registerNamespaces()
    for specConfig in shaclSpecsConfig:
        generateFromSpec(specConfig)

    logging.info('Conversion finished')
