describe('Add new record', () => {

  it('creates a new record based on dataset / open / non-geo template', () => {
    // first login
    cy.visit('/')
    cy.acceptCookies()
    cy.login()
    // load the create record view
    cy.visit('/srv/eng/catalog.edit#/create')
    // click the 'dataset' item
    cy.get('.col-sm-2 > .panel > .panel-body > .list-group').contains('dataset').click()
    cy.get('.col-sm-4 > .panel-default > .panel-body > .list-group').contains('Open data (niet-geo)').click()
    cy.get('[type="button"][data-gn-click-and-spin="createNewMetadata(true)"]').click()
    cy.get('.nav-tabs >> a').contains('Dataset').should('exist')
    cy.get('.nav-tabs >> a').contains('Distributions').should('exist')
    cy.get('.nav-tabs >> a').contains('Record').should('exist')
    // cancel the creation
    cy.get('#gn-editor-btn-cancel').click()
  })
})
