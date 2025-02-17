import json
import logging
import xml.etree.ElementTree as ET
from os.path import abspath
from xml.dom import minidom

import requests

from constants import dcatNamespaces, fullnameSwaps, schNamespaces, uriSwaps


def loadJsonUrl(url):
    if url.startswith('http://') or url.startswith('https://'):
        text = requests.get(url).text
    else:
        file_path = abspath(url)
        logging.debug('Reading file ' + file_path)
        file = open(file_path, 'r')
        text = file.read()
        file.close()

    return json.loads(text)


def getFullName(uri):
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
        raise Exception('Could not find namespace for uri ' + uri)


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
