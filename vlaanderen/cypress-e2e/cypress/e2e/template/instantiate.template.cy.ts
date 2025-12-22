describe('Chai', () => {

  it('can assert the nested "valid" property to be 1', () => {
    let testObject = {
      "response": {
        "body": {
          "hits": {
            "hits": [
              {
                "_source": {
                  "documentStandard": "dcat-ap",
                  "valid": "1",
                }
              }
            ]
          }
        }
      }
    }
    expect(testObject).to.nested.include({'response.body.hits.hits[0]._source.valid': '1'})
  })

})


describe('Templates', () => {

  beforeEach(() => {
    cy.visit('/')
    cy.ensureReindex()
    cy.ensureTemplates()
  })

  it('allow creating a valid DCAT-AP-VLv2 dataset', () => {
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
    cy.visit('/srv/dut/catalog.edit#/create')

    // when
    // create a new dcat-ap-vl2 dataset record that correctly validates
    cy.get('a').contains('DCAT-AP VL v2.0').click()
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

    // then
    // the record is valid
    cy.get('button#gn-editor-btn-save').click({force: true})
    cy.wait(1000)
    cy.get('button').contains('Valideren').click()
    cy.wait(1000)
    cy.intercept('POST', '/srv/api/search/records/_search').as('validation')
    cy.get('button').contains('Valideren').click()
    cy.get('button[title="hideSuccess"]').click()
    cy.wait('@validation').its('response.body').should('nested.include', {'hits.hits[0]._source.valid': '1'})
  })

})
