describe('Workflow', () => {

  beforeEach(() => {
    cy.visit('/')
    cy.ensureReindex()
    cy.ensureTemplates()
  })

  it('uses chai nested include to test valid property to be 1', () => {
    let testObject = {
      "id": "interceptedRequest17902",
      "browserRequestId": "347401.18400",
      "routeId": "1761921252896-2061",
      "request": {
        "headers": {
          "host": "localhost:8080",
          "proxy-connection": "keep-alive",
          "content-length": "160",
          "sec-ch-ua-platform": "\"Linux\"",
          "x-xsrf-token": "7839cc7b-f569-4a9c-952a-b4f9e0b40f3a",
          "accept-language": "dut",
          "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\"",
          "sec-ch-ua-mobile": "?0",
          "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Cypress/15.5.0 Chrome/138.0.7204.251 Electron/37.6.0 Safari/537.36",
          "accept": "application/json, text/plain, */*",
          "content-type": "application/json;charset=UTF-8",
          "origin": "http://localhost:8080",
          "sec-fetch-site": "same-origin",
          "sec-fetch-mode": "cors",
          "sec-fetch-dest": "empty",
          "referer": "http://localhost:8080/srv/dut/catalog.edit",
          "accept-encoding": "gzip, deflate, br, zstd",
          "cookie": "XSRF-TOKEN=7839cc7b-f569-4a9c-952a-b4f9e0b40f3a; JSESSIONID=node01pbs2retl0cxm1tkyg63if849d424.node0; serverTime=1761921253112; sessionExpiry=1761932053112"
        },
        "url": "http://localhost:8080/srv/api/search/records/_search",
        "method": "POST",
        "httpVersion": "1.1",
        "resourceType": "xhr",
        "query": {},
        "body": {
          "query": {
            "bool": {
              "must": [
                {
                  "multi_match": {
                    "query": "1381",
                    "fields": [
                      "id^2",
                      "uuid"
                    ]
                  }
                },
                {
                  "terms": {
                    "draft": [
                      "n",
                      "y",
                      "e"
                    ]
                  }
                },
                {
                  "terms": {
                    "isTemplate": [
                      "n",
                      "y",
                      "s"
                    ]
                  }
                }
              ]
            }
          }
        },
        "responseTimeout": 30000,
        "alias": "validation"
      },
      "state": "Complete",
      "requestWaited": true,
      "responseWaited": true,
      "subscriptions": [],
      "response": {
        "headers": {
          "date": "Fri, 31 Oct 2025 14:34:13 GMT",
          "set-cookie": [
            "serverTime=1761921253778; Path=/",
            "sessionExpiry=1761932053778; Path=/"
          ],
          "expires": "Thu, 01 Jan 1970 00:00:00 GMT",
          "access-control-allow-origin": "*",
          "access-control-allow-headers": "X-Requested-With, Content-Type",
          "access-control-allow-credentials": "true",
          "vary": "Origin",
          "x-frame-options": "SAMEORIGIN",
          "content-security-policy": "frame-ancestors 'self'",
          "content-encoding": "gzip",
          "content-type": "application/json",
          "transfer-encoding": "chunked",
          "server": "Jetty(9.4.54.v20240208)"
        },
        "url": "http://localhost:8080/srv/api/search/records/_search",
        "method": null,
        "httpVersion": "1.1",
        "statusCode": 200,
        "statusMessage": "OK",
        "body": {
          "took": 1,
          "timed_out": false,
          "_shards": {
            "total": 1,
            "successful": 1,
            "skipped": 0,
            "failed": 0
          },
          "hits": {
            "total": {
              "value": 1,
              "relation": "eq"
            },
            "max_score": 7.831379,
            "hits": [
              {
                "_index": "gn-records",
                "_id": "9e815650-1e13-44a7-a743-1332c9ae97f8",
                "_score": 7.831379,
                "_source": {
                  "docType": "metadata",
                  "dateStamp": "2025-10-30T23:00:00.000Z",
                  "metadataIdentifier": "9e815650-1e13-44a7-a743-1332c9ae97f8",
                  "OrgObject": [
                    {
                      "default": "agentschap Digitaal Vlaanderen",
                      "langdut": "agentschap Digitaal Vlaanderen",
                      "link": "https://localhost:8080/geonetwork/srv/resources/organizations/agentschap%20Digitaal%20Vlaanderen"
                    },
                    {
                      "default": "agentschap Digitaal Vlaanderen",
                      "langdut": "agentschap Digitaal Vlaanderen"
                    }
                  ],
                  "publisherOrgObject": {
                    "default": "agentschap Digitaal Vlaanderen",
                    "langdut": "agentschap Digitaal Vlaanderen",
                    "link": "https://localhost:8080/geonetwork/srv/resources/organizations/agentschap%20Digitaal%20Vlaanderen"
                  },
                  "contact": [
                    {
                      "organisationObject": {
                        "default": "agentschap Digitaal Vlaanderen",
                        "langdut": "agentschap Digitaal Vlaanderen",
                        "link": "https://localhost:8080/geonetwork/srv/resources/organizations/agentschap%20Digitaal%20Vlaanderen"
                      },
                      "role": "publisher",
                      "email": "",
                      "phone": ""
                    },
                    {
                      "organisationObject": {
                        "default": "agentschap Digitaal Vlaanderen",
                        "langdut": "agentschap Digitaal Vlaanderen"
                      },
                      "role": "pointOfContact",
                      "email": "mailto:digitaal.vlaanderen@vlaanderen.be",
                      "website": "https://www.vlaanderen.be/digitaal-vlaanderen",
                      "individual": "",
                      "phone": "",
                      "address": ""
                    }
                  ],
                  "pointOfContactOrgObject": {
                    "default": "agentschap Digitaal Vlaanderen",
                    "langdut": "agentschap Digitaal Vlaanderen"
                  },
                  "resourceType": [
                    "dataset"
                  ],
                  "standardNameObject": {
                    "default": "DCAT-AP Vlaanderen",
                    "langdut": "DCAT-AP Vlaanderen",
                    "lang": "DCAT-AP Flanders"
                  },
                  "resourceTitleObject": {
                    "default": "abc123",
                    "langdut": "abc123"
                  },
                  "resourceAbstractObject": {
                    "default": "ABC123",
                    "langdut": "ABC123"
                  },
                  "indexingDate": "2025-10-31T15:34:13+01:00",
                  "OrgForResourceObject": {
                    "default": "Organisation Name",
                    "langdut": "Organisation Name"
                  },
                  "publisherOrgForResourceObject": {
                    "default": "Organisation Name",
                    "langdut": "Organisation Name"
                  },
                  "contactForResource": [
                    {
                      "organisationObject": {
                        "default": "Organisation Name",
                        "langdut": "Organisation Name"
                      },
                      "role": "publisher",
                      "email": "",
                      "phone": ""
                    },
                    {
                      "role": "pointOfContact",
                      "email": "mailto:a@b.c",
                      "website": "",
                      "individual": "",
                      "phone": "",
                      "address": ""
                    }
                  ],
                  "rdfResourceIdentifier": "http://localhost:8080/srv/resources/datasets/96f7903e-49d6-4799-8133-33dd5824024b",
                  "resourceIdentifier": [
                    {
                      "code": "96f7903e-49d6-4799-8133-33dd5824024b",
                      "codeSpace": "",
                      "link": "http://localhost:8080/srv/resources/datasets/96f7903e-49d6-4799-8133-33dd5824024b"
                    }
                  ],
                  "mainLanguage": "dut",
                  "otherLanguage": [
                    "dut"
                  ],
                  "resourceLanguage": [
                    "dut"
                  ],
                  "tagNumber": "2",
                  "tag": [
                    {
                      "default": "Keyword 1",
                      "langdut": "Keyword 1"
                    },
                    {
                      "default": "Vlaamse Open data",
                      "langdut": "Vlaamse Open data",
                      "langeng": "Vlaamse Open data",
                      "langfre": "Vlaamse Open data",
                      "langger": "Vlaamse Open data",
                      "link": "https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden/VLOPENDATA",
                      "key": "https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden/VLOPENDATA"
                    }
                  ],
                  "th_access-rightNumber": "1",
                  "th_access-right": [
                    {
                      "default": "publiek",
                      "langdut": "publiek",
                      "link": "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                    }
                  ],
                  "th_access-right_tree": [
                    {
                      "key": [
                        "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                      ],
                      "default": [
                        "publiek"
                      ]
                    }
                  ],
                  "th_GDI-Vlaanderen-trefwoordenNumber": "1",
                  "th_GDI-Vlaanderen-trefwoorden": [
                    {
                      "default": "Vlaamse Open data",
                      "langdut": "Vlaamse Open data",
                      "langeng": "Vlaamse Open data",
                      "langfre": "Vlaamse Open data",
                      "langger": "Vlaamse Open data",
                      "link": "https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden/VLOPENDATA"
                    }
                  ],
                  "th_GDI-Vlaanderen-trefwoorden_tree": [
                    {
                      "key": [
                        "https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden/VLOPENDATA"
                      ],
                      "default": [
                        "Vlaamse Open data"
                      ]
                    }
                  ],
                  "th_otherKeywords-Number": 1,
                  "th_otherKeywords": [
                    {
                      "default": "Keyword 1",
                      "langdut": "Keyword 1"
                    }
                  ],
                  "allKeywords": {
                    "th_otherKeywords": {
                      "title": "otherKeywords-",
                      "theme": "",
                      "keywords": [
                        {
                          "default": "Keyword 1",
                          "langdut": "Keyword 1"
                        }
                      ]
                    },
                    "th_access-right": {
                      "id": "external.theme.access-right",
                      "title": "Access rights",
                      "theme": "theme",
                      "link": "http://publications.europa.eu/resource/authority/access-right",
                      "keywords": [
                        {
                          "default": "publiek",
                          "langdut": "publiek",
                          "link": "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                        }
                      ]
                    },
                    "th_GDI-Vlaanderen-trefwoorden": {
                      "id": "external.theme.GDI-Vlaanderen-trefwoorden",
                      "title": "GDI-Vlaanderen Trefwoorden",
                      "theme": "theme",
                      "link": "https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden",
                      "keywords": [
                        {
                          "default": "Vlaamse Open data",
                          "langdut": "Vlaamse Open data",
                          "langeng": "Vlaamse Open data",
                          "langfre": "Vlaamse Open data",
                          "langger": "Vlaamse Open data",
                          "link": "https://metadata.vlaanderen.be/id/GDI-Vlaanderen-Trefwoorden/VLOPENDATA"
                        }
                      ]
                    }
                  },
                  "MD_LegalConstraintsOtherConstraintsObject": [
                    {
                      "default": "publiek",
                      "langdut": "publiek",
                      "link": "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                    },
                    {
                      "default": "publiek",
                      "langdut": "publiek",
                      "link": "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                    }
                  ],
                  "linkUrl": "https://a.b",
                  "link": [
                    {
                      "protocol": "",
                      "mimeType": "",
                      "url": "https://a.b",
                      "name": "Distribution 1 title",
                      "description": "Distribution 1 description",
                      "function": "",
                      "applicationProfile": "",
                      "group": 0
                    }
                  ],
                  "hasOverview": "false",
                  "referenceDate": "0000-01-01T00:00:00.000Z",
                  "vlResourceConstraintsObject": [
                    {
                      "type": "MD_LegalConstraints",
                      "otherConstraintsObject": [
                        {
                          "default": "publiek",
                          "langdut": "publiek",
                          "link": "http://publications.europa.eu/resource/authority/access-right/PUBLIC"
                        }
                      ]
                    }
                  ],
                  "isOpenData": "true",
                  "isGeoData": "n",
                  "statusWorkflowPublished": "draft",
                  "valid_schematron-rules-dcat-ap": "1",
                  "valid_schematron-rules-dcat-ap-vl": "1",
                  "valid_inspire": "-1",
                  "uuid": "9e815650-1e13-44a7-a743-1332c9ae97f8",
                  "displayOrder": "0",
                  "popularity": "0",
                  "isPublishedToAll": "false",
                  "record": "record",
                  "draft": "n",
                  "changeDate": "2025-10-31T14:34:13.134046Z",
                  "id": "1381",
                  "valid_xsd": "1",
                  "nonOgcwxsSourceCatalog": "c678d0fb-894d-403f-b146-4b96706a1a16",
                  "isPublishedToIntranet": "false",
                  "valid_schematron-rules-dcat-ap-cardinalities": "1",
                  "groupOwnerName": "Digitaal Vlaanderen",
                  "valid_schematron-rules-dcat-ap-vl-cardinalities": "1",
                  "groupOwnerVlType": "metadatavlaanderen",
                  "featureOfRecord": "record",
                  "isPublishedToGuest": "false",
                  "documentStandard": "dcat-ap",
                  "valid": "1",
                  "isTemplate": "n",
                  "feedbackCount": "0",
                  "rating": "0",
                  "valid_schematron-rules-dcat-ap-rec": "1",
                  "isHarvested": "false",
                  "valid_schematron-rules-dcat-ap-vl-rec": "0",
                  "recordOwner": "mdv admin",
                  "groupPublishedId": "102",
                  "userinfo": "mdv|admin|mdv|Administrator",
                  "groupPublished": "Digitaal Vlaanderen",
                  "valid_schematron-rules-mdcat": "1",
                  "createDate": "2025-10-31T14:33:55.055689Z",
                  "owner": "1",
                  "statusWorkflow": "draft",
                  "groupOwner": "102",
                  "logo": "/images/logos/c678d0fb-894d-403f-b146-4b96706a1a16.png",
                  "mdStatus": "1",
                  "hasxlinks": "false",
                  "op0": "102",
                  "op2": "102",
                  "op1": "102",
                  "extra": "null",
                  "op3": "102",
                  "valid_schematron-rules-mdcat-rec": "1",
                  "op5": "102",
                  "mdStatusChangeDate": "2025-10-31T14:33:55.166888Z",
                  "userSavedCount": "0",
                  "sourceCatalogue": "c678d0fb-894d-403f-b146-4b96706a1a16"
                },
                "ownerId": 1,
                "edit": true,
                "canReview": true,
                "owner": true,
                "isPublishedToAll": false,
                "view": true,
                "notify": true,
                "download": true,
                "dynamic": true,
                "featured": true,
                "selected": false
              }
            ]
          }
        }
      }
    }
    expect(testObject).to.nested.include({'response.body.hits.hits[0]._source.valid': '1'})
  })

  it('allows to create a draft that can be published by an admin', () => {
    // given
    cy.visit('/')
    cy.loginAdmin()
    let title = 'abc123'
    let description = 'ABC123'
    let agentName = 'Organisation Name'
    let keyword = 'Keyword 1'
    let email = 'a@b.c'
    let distributionTitle = 'Distribution 1 title'
    let distributionDescription = 'Distribution 1 description'
    let distributionUrl = 'https://a.b'

    // when
    // create a new dcat-ap-vl2 dataset record that correctly validates
    cy.visit('/srv/dut/catalog.edit#/create')
    cy.get('a').contains('Generieke Open data, conform DCAT-AP VL v2.0').click()
    cy.get('select[data-ng-model="selectedGroup"]').select('Digitaal Vlaanderen')
    cy.get('button').contains('Aanmaken').click()
    cy.get('fieldset.gn-basicInformation div.gn-title input').type(title)
    cy.get('fieldset.gn-basicInformation div.gn-description textarea').type(description)
    cy.get('fieldset.gn-Agent div.gn-name input').type(agentName)
    cy.get('fieldset.gn-basicInformation div.gn-keyword input').type(keyword)
    cy.get('fieldset.gn-usageInformation fieldset.gn-contactPoint fieldset.gn-Organization label').contains('E-mail').parent().within(() => {
      cy.get('input[type="text"]').type(email)
    })
    cy.get('li[role="menuitem"]').contains('Distributies').click()
    cy.get('div.gn-title input').type(distributionTitle)
    cy.get('div.gn-description textarea').type(distributionDescription)
    cy.get('input[data-gn-field-tooltip="dcat-ap|dcat:accessURL"]').type(distributionUrl)

    cy.get('button#gn-editor-btn-save').click()
    cy.wait(1000)
    cy.get('button').contains('Valideren').click()
    cy.wait(1000)
    cy.intercept('POST', '/srv/api/search/records/_search').as('validation')
    cy.get('button').contains('Valideren').click()
    cy.get('button[title="hideSuccess"]').click()
    // cy.wait('@validation').should('nested.include', {'response.body.hits.hits[0]._source.valid': '1'})
    cy.wait('@validation').its('response.body').should('nested.include', {'hits.hits[0]._source.valid': '1'})
  })
})
