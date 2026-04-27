shaclSpecsConfig = [
    {
        'name': 'schematron-rules-mdcat',
        # 'level': 'sh:Violation',
        'title': {
            'dut': 'Metadata DCAT - Verplicht',
            'eng': 'Metadata DCAT - Mandatory',
            'fre': 'Metadata DCAT - Obligatoire',
            'ger': 'Metadata DCAT - Obligatorisch'
        },
        'url': 'https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat/erkendestandaard/2022-04-21/shacl/metadata-voor-services-ap-SHACL.ttl',
        'profile': 'https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat'
    },
    {
      'name': 'schematron-rules-mdcat-rec',
      'level': 'sh:Warning',
      'title': {
        'dut': 'Metadata DCAT - Aanbevolen',
        'eng': 'Metadata DCAT - Recommended',
        'fre': 'Metadata DCAT - Recommandé',
        'ger': 'Metadata DCAT - Empfohlen'
      },
      'url': 'https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat/erkendestandaard/2022-04-21/shacl/metadata-voor-services-ap-SHACL.ttl',
      'profile': 'https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat'
    },
    # {
    #     'name': 'schematron-rules-dcat-ap-vl',
    #     'level': 'sh:Violation',
    #     'title': {
    #         'dut': 'DCAT-AP-Vlaanderen - Verplicht',
    #         'eng': 'DCAT-AP-Vlaanderen - Mandatory',
    #         'fre': 'DCAT-AP-Vlaanderen - Obligatoire',
    #         'ger': 'DCAT-AP-Vlaanderen - Obligatorisch'
    #     },
    #     'url': 'https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL/erkendestandaard/2026-02-12/shacl/DCAT-AP-VL-SHACL.ttl',
    #     'profile': 'https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL'
    # },
    # {
    #   'name': 'schematron-rules-dcat-ap-vl',
    #   'level': 'sh:Warning',
    #   'title': {
    #     'dut': 'DCAT-AP-Vlaanderen - Aanbevolen',
    #     'eng': 'DCAT-AP-Vlaanderen - Recommended',
    #     'fre': 'DCAT-AP-Vlaanderen - Recommandé',
    #     'ger': 'DCAT-AP-Vlaanderen - Empfohlen'
    #   },
    #   'url': 'https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL/erkendestandaard/2026-02-12/shacl/DCAT-AP-VL-SHACL.ttl',
    #   'profile': 'https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL'
    # },
    {
      'name': 'schematron-rules-mobility-110',
      'level': 'sh:Violation',
      'title': {
        'dut': 'Mobility (v1.1.0)',
        'eng': 'Mobility (v1.1.0)',
        'fre': 'Mobility (v1.1.0)',
        'ger': 'Mobility (v1.1.0)',
      },
      'url': 'https://raw.githubusercontent.com/mobilityDCAT-AP/mobilityDCAT-AP/refs/heads/gh-pages/releases/1.1.0/shaclShapes/mobilitydcat-ap_shacl_shapes.ttl',
      'profile': 'https://w3id.org/mobilitydcat-ap/releases/1.1.0/'
    },
  {
    'name': 'schematron-rules-mobility-110-rec',
    'level': 'sh:Warning',
    'title': {
      'dut': 'Mobility - Recommended (v1.1.0)',
      'eng': 'Mobility - Recommended (v1.1.0)',
      'fre': 'Mobility - Recommended (v1.1.0)',
      'ger': 'Mobility - Recommended (v1.1.0)',
    },
    'url': 'https://raw.githubusercontent.com/mobilityDCAT-AP/mobilityDCAT-AP/refs/heads/gh-pages/releases/1.1.0/shaclShapes/mobilitydcat-ap_shacl_shapes.ttl',
    'profile': 'https://w3id.org/mobilitydcat-ap/releases/1.1.0/'
  }
    # {
    #     'name': 'schematron-rules-mdcat-rec',
    #     'title': {
    #         'dut': 'Aanbevolen metadata-dcat',
    #         'eng': 'Recommended metadata-dcat',
    #         'fre': 'Recommended metadata-dcat',
    #         'ger': 'Recommended metadata-dcat',
    #     },
    #     'url': 'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/validation/release/metadata_dcat.jsonld',
    #     'profile': 'https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat',
    #     'level': 'sh:Warning'
    # },
    # {
    #     'name': 'schematron-rules-dcat-ap-vl',
    #     'title': {
    #         'dut': 'Bijkomende vereisten van DCAT-AP-Vlaanderen',
    #         'eng': 'Mandatory DCAT-AP-Vl Rules',
    #         'fre': 'Mandatory DCAT-AP-Vl Rules',
    #         'ger': 'Mandatory DCAT-AP-Vl Rules',
    #     },
    #
    #     'url': [
    #         'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/validation/release/dcatapvl.jsonld',
    #         # 'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/validation/release/dcatapvl-usagenotes.jsonld'
    #         'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/6b6cc4a86c33f640b2d9825ff33f5dbb25251137/release/dcatapvl-usagenotes.jsonld'
    #     ],
    #     'profile': 'https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL'
    # },
    # {
    #     'name': 'schematron-rules-dcat-ap-vl-rec',
    #     'title': {
    #         'dut': 'Aanbevolen DCAT-AP-Vlaanderen',
    #         'eng': 'Recommended DCAT-AP-Vl Rules',
    #         'fre': 'Recommended DCAT-AP-Vl Rules',
    #         'ger': 'Recommended DCAT-AP-Vl Rules',
    #     },
    #     'url': [
    #         'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/validation/release/dcatapvl.jsonld',
    #         # 'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/validation/release/dcatapvl-usagenotes.jsonld'
    #         'https://raw.githubusercontent.com/Informatievlaanderen/OSLOthema-metadataVoorServices/6b6cc4a86c33f640b2d9825ff33f5dbb25251137/release/dcatapvl-usagenotes.jsonld'
    #     ],
    #     'profile': 'https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL',
    #     'level': 'sh:Warning'
    # },
    # {
    #     'name': 'schematron-rules-dcat-ap',
    #     'title': {
    #         'dut': 'Aanbevolen DCAT-AP',
    #         'eng': 'Recommended DCAT-AP Rules',
    #         'fre': 'Recommended DCAT-AP Rules',
    #         'ger': 'Recommended DCAT-AP Rules',
    #     },
    #     'url': [
    #         'https://semiceu.github.io/DCAT-AP/releases/3.0.0/html/shacl/shapes_recommended.ttl'
    #     ],
    #     'profile': 'http://data.europa.eu/r5r#',
    #     'level': 'sh:Warning'
    # }
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
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'sh': 'http://www.w3.org/ns/shacl#',
    'mobilitydcatap': 'https://w3id.org/mobilitydcat-ap',
    'oa': 'http://www.w3.org/ns/oa',
    'content': 'http://www.w3.org/2011/content',
    'org': 'http://www.w3.org/ns/org',
    'dcat-ap': 'http://data.europa.eu/r5r/',
    'dqv': 'http://www.w3.org/ns/dqv'
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

