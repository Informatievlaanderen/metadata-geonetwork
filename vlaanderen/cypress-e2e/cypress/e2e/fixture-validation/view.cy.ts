describe('Check expected content in view', () => {

  before(() => {
    // set up
    cy.visit('/')
    cy.loginAdmin()
    // make sure the record is present
    cy.deleteRecord('cypress-test-0001')
    cy.importXml('dcatapvl2-dataset.xml')
  })

  beforeEach(() => {
    cy.visit('/')
    cy.acceptCookies()
    cy.loginAdmin()
  })

  it('Validates structure of the DCAT-AP-VL v2 Dataset view.', () => {
    // load the create record view
    cy.visit('/srv/dut/catalog.search#/metadata/cypress-test-0001')

    // test tabs are there
    cy.get('.nav-tabs a').contains('Dataset').should('exist')
    cy.get('.nav-tabs a').contains('Distributies').should('exist')
    cy.get('.nav-tabs a').contains('Record').should('exist')
  })

  it('Validates shown content of the DCAT-AP-VL v2 Dataset.', () => {
    // load the create record view
    cy.visit('/srv/dut/catalog.search#/metadata/cypress-test-0001')

    // check dataset title
    let title = cy.get('#gn-tab-tabDataset td').contains('[cypress] - DCAT-AP-VL Dataset - v2 - NL')
    title.should('exist')
    title.siblings('th').contains('Titel').should('exist')

    // check dataset description
    let description = cy.get('#gn-tab-tabDataset td').contains('Test record aangemaakt door Cypress voor end-to-end testing mogelijk te maken.')
    description.should('exist')
    description.siblings('th').contains('Beschrijving').should('exist')

    // check keywords
    let keyword = cy.get('#gn-tab-tabDataset th.gn-keyword').contains('Trefwoord');
    keyword.should('exist')
    keyword.siblings('td').within(() => {
      cy.get('div a').contains("cypressNL").should("exist")
      cy.get('div a').contains("cypressEN").should("exist")
    })

    // check distribution info
    let distributionTitle = cy.get('#gn-tab-tabDistribution td').contains('Distributie één')
    distributionTitle.should('exist')
    distributionTitle.siblings('th').contains('Titel').should('exist')

    // check headers shown
    let headers = ['Titel', 'Beschrijving', 'URI', 'Naam', 'Type', 'Trefwoord', 'Identificator', 'MAGDA-categorie', 'Statuut', 'Thema', 'Versie', 'Creatiedatum', 'Wijzigingsdatum', 'Publicatiedatum', 'URI', 'Naam Contactpunt', 'Organisatienaam', 'Adres', 'E-mail', 'Website', 'Telefoonnummer', 'Toegankelijkheid', 'Rechten', 'Locatie', 'Temporele begrenzing', 'Taal', 'Conformiteit met standaard']
    headers.forEach(header => {
      cy.get('div.gn-tab-content th').contains(header)
    })

    // check english title
    cy.visit('/srv/eng/catalog.search#/metadata/cypress-test-0001')
    let englishTitle = cy.get('#gn-tab-tabDataset td').contains('[cypress] - DCAT-AP-VL Dataset - v2 - EN')
    englishTitle.should('exist')
    englishTitle.siblings('th').contains('Title').should('exist')
  })
})
