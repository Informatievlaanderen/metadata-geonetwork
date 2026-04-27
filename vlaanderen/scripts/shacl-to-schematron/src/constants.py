import os
import yaml


def _loadConfig():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
    with open(config_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data.get('specs', [])


shaclSpecsConfig = _loadConfig()

schOutput = '../core-geonetwork/schemas/dcat2/src/main/plugin/dcat2/schematron'
locOutput = '../core-geonetwork/schemas/dcat2/src/main/plugin/dcat2/loc'

schNamespaces = {
    'sch': 'http://purl.oclc.org/dsdl/schematron',
    'xsl': 'http://www.w3.org/1999/XSL/Transform',
    'xs': 'http://www.w3.org/2001/XMLSchema#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'
}

dcatNamespaces = {
    'spdx': 'http://spdx.org/rdf/terms#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'adms': 'http://www.w3.org/ns/adms#',
    'locn': 'http://www.w3.org/ns/locn#',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'foaf': 'http://xmlns.com/foaf/0.1/',
    'dct': 'http://purl.org/dc/terms/',
    'vcard': 'http://www.w3.org/2006/vcard/ns#',
    'dcat': 'http://www.w3.org/ns/dcat#',
    'schema': 'http://schema.org/',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'skos': 'http://www.w3.org/2004/02/skos/core#',
    'xml': 'http://www.w3.org/XML/1998/namespace',
    'gco': 'http://www.isotc211.org/2005/gco',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'geonet': 'http://www.fao.org/geonetwork',
    'xlink': 'http://www.w3.org/1999/xlink',
    'mdcat': 'https://data.vlaanderen.be/ns/metadata-dcat#',
    'geodcat': 'http://data.europa.eu/930/',
    'generiek': 'http://data.vlaanderen.be/ns/generiek#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'sh': 'http://www.w3.org/ns/shacl#',
    'mobilitydcatap': 'https://w3id.org/mobilitydcat-ap',
    'oa': 'http://www.w3.org/ns/oa',
    'content': 'http://www.w3.org/2011/content',
    'org': 'http://www.w3.org/ns/org',
    'dcat-ap': 'http://data.europa.eu/r5r/',
    'dqv': 'http://www.w3.org/ns/dqv',
    'eli': 'http://data.europa.eu/eli/ontology',
    'time': 'http://www.w3.org/2006/time'
}

fullnameSwaps = {
    'vcard:Kind': 'vcard:Organization',
    'dct:Agent': 'foaf:Agent',
    'schema:ContactPoint': 'vcard:Organization',
    'mdcat:bronMetadataRecordLandingspagina': 'mdcat:landingpageVoorBronMetadata'
}

omitRules = [
    'https://data.vlaanderen.be/shacl/metadata_dcat#CatalogusRecordShape/0311d40d6c8081dc49766336ad753baee5d276f2'
]

expressions = {
    'uri': "'^\\w+:(/?/?)[^\\s]+$'",
    'dateAndDateTime': "'^\\d{4}-\\d{2}-\\d{2}(Z|(-|\\+)\\d{2}:\\d{2}|T\\d{2}:\\d{2}:\\d{2}(\\.\\d+)?(Z|(-|\\+)\\d{2}:\\d{2})?)?$'"
}

uriSwaps = {
    'https://vocab.belgif.be/auth/datatheme': 'http://vocab.belgif.be/auth/datatheme'
}

primaryLanguage = 'nl'
fallbackLanguages = ['en']
