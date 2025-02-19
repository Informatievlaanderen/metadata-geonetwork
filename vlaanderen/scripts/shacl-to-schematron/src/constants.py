shaclSpecsConfig = [
    {
        'name': 'schematron-rules-mdcat',
        'title': {
            'dut': 'Bijkomende vereisten van metadata-dcat',
            'eng': 'Mandatory metadata-dcat Rules',
            'fre': 'Mandatory metadata-dcat Rules',
            'ger': 'Mandatory metadata-dcat Rules',
        },
        'url': 'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/validation/release/metadata_dcat.jsonld',
        'profile': 'https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat'
    },
    {
        'name': 'schematron-rules-mdcat-rec',
        'title': {
            'dut': 'Aanbevolen metadata-dcat',
            'eng': 'Recommended metadata-dcat',
            'fre': 'Recommended metadata-dcat',
            'ger': 'Recommended metadata-dcat',
        },
        'url': 'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/validation/release/metadata_dcat.jsonld',
        'profile': 'https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat',
        'level': 'sh:Warning'
    },
    {
        'name': 'schematron-rules-dcat-ap-vl',
        'title': {
            'dut': 'Bijkomende vereisten van DCAT-AP-Vlaanderen',
            'eng': 'Mandatory DCAT-AP-Vl Rules',
            'fre': 'Mandatory DCAT-AP-Vl Rules',
            'ger': 'Mandatory DCAT-AP-Vl Rules',
        },

        'url': [
            'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/validation/release/dcatapvl.jsonld',
            # 'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/validation/release/dcatapvl-usagenotes.jsonld'
            'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/6b6cc4a86c33f640b2d9825ff33f5dbb25251137/release/dcatapvl-usagenotes.jsonld'
        ],
        'profile': 'https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL'
    },
    {
        'name': 'schematron-rules-dcat-ap-vl-rec',
        'title': {
            'dut': 'Aanbevolen DCAT-AP-Vlaanderen',
            'eng': 'Recommended DCAT-AP-Vl Rules',
            'fre': 'Recommended DCAT-AP-Vl Rules',
            'ger': 'Recommended DCAT-AP-Vl Rules',
        },
        'url': [
            'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/validation/release/dcatapvl.jsonld',
            # 'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/validation/release/dcatapvl-usagenotes.jsonld'
            'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/6b6cc4a86c33f640b2d9825ff33f5dbb25251137/release/dcatapvl-usagenotes.jsonld'
        ],
        'profile': 'https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL',
        'level': 'sh:Warning'
    }
]

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
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#'
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
