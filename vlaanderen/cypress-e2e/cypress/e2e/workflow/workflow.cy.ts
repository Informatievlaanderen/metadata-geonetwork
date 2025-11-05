describe('Workflow', () => {

  before(() => {
    cy.ensureReindex()
    cy.ensureTemplates()
  })

  /**
   * All these tests start from a fresh copy in draft status.
   * this.metadataId is available to know about the new record.
   */
  beforeEach(() => {
    createFreshCopy()
  })

  /**
   * Clean up the records we have created.
   */
  afterEach(function () {
    // delete, although it could have been deleted by a test already
    cy.deleteRecord(this.uuid)
  })

  let createFreshCopy = function () {
    // create a fresh copy of an existing record
    cy.loginEditor()
    cy.visit('/')
    cy.acceptCookies()
    cy.visit('/srv/dut/catalog.edit#/create?from=104')
    cy.get('button').contains('Aanmaken').click()
    cy.get('div.gn-title input').as('titleInput')
    // need to add the timeout here, otherwise the title is sometimes empty after clicking save
    cy.get('@titleInput').type('cypress workflow test record', {timeout: 1000})
    cy.url().then((url: string) => {
      let regex = new RegExp('.*catalog.edit#/metadata/([0-9]+)\\?.*$', "g");
      let matches = regex.exec(url);
      expect(matches).to.have.length(2);
      let metadataId = +matches[1]
      cy.wrap(metadataId)
        .should('be.a', 'number')
        .should('be.at.least', 1)
        // make it available as this.metadataId in the tests
        .as('metadataId')
      cy.intercept({
        method: 'POST',
        pathname: '**/editor*'
      }).as('savePost')
      cy.get('#gn-editor-btn-save').click()
      cy.wait('@savePost')
      cy.get('#gn-editor-btn-close').click()
      cy.visit(`/srv/dut/catalog.search#/metadata/${metadataId}`)
      cy.url().then((url: string) => {
        let matches = new RegExp('.*catalog.search#/metadata/(.+)').exec(url);
        expect(matches).to.have.length(2);
        let uuid = matches[1]
        cy.wrap(uuid)
          .should('be.a', 'string')
          .as('uuid')
      })
    })
  }

  it('shows only the relevant options for editors', function () {
    cy.loginEditor()
    cy.visit(`/srv/dut/catalog.search#/metadata/${this.metadataId}`)

    // open the workflow dropdown
    cy.get('h1 span.badge').contains('In ontwerp')
    cy.get('#gn-button-manage-record').click()
    cy.get('li[data-ng-repeat="step in getStatusEffects(user)"]:visible').should('have.length', 2)
    cy.get('li[data-ng-repeat="step in getStatusEffects(user)"]').contains('Ingediend voor publicatie')
    cy.get('li[data-ng-repeat="step in getStatusEffects(user)"]').contains('Verwijderd')

    // apply for validation
    cy.get('li[data-ng-repeat="step in getStatusEffects(user)"]').contains('Ingediend voor publicatie').click()
    cy.get('button').contains('Ingediend voor publicatie').click()

    // can only go for deletion now
    cy.get('h1 span.badge').contains('Ingediend voor publicatie')
    cy.get('#gn-button-manage-record').click()
    cy.get('li[data-ng-repeat="step in getStatusEffects(user)"]:visible').should('have.length', 1)
    cy.get('li[data-ng-repeat="step in getStatusEffects(user)"]').contains('Verwijderd')
  })

  it('allows deletion of a record', function () {
    cy.loginEditor()
    cy.visit(`/srv/dut/catalog.search#/metadata/${this.metadataId}`)
    cy.get('#gn-button-manage-record').click()
    cy.get('li[data-ng-repeat="step in getStatusEffects(user)"]').contains('Verwijderd').click()
    cy.get('button').contains('Verwijderd').click()
    // validate that the record is actually gone
    cy.log(`check that ${this.uuid} was deleted...`)
    cy.request({
      url: `/srv/api/records/${this.uuid}`,
      failOnStatusCode: false
    }).its('status').should('be.oneOf', [400, 404])
  })
})
