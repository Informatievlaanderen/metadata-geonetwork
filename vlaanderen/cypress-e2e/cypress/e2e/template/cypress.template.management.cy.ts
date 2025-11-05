describe('Template cypress management', () => {

  it('can correctly reload templates without touching other records.', () => {
    // check we have at least an expected amount of non-draft records
    cy.recordCount(false, null).should('be.at.least', 5).as('beforeCount')
    // templates should be 0 after deleting them
    cy.deleteTemplates()
    cy.recordCount(false, true).should('equal', 0)
    cy.ensureTemplates()
    cy.recordCount(false, true).should('be.at.least', 10)
    cy.deleteTemplates()
    cy.recordCount(false, true).should('equal', 0)
    cy.get('@beforeCount').then((beforeCount) => {
      cy.recordCount(false, null).should('equal', beforeCount)
    })
  })
})
