describe('login', () => {
  beforeEach('passes', () => {
    cy.visit(`/`)
    cy.acceptCookies()
    // should be able to run this function twice without crashing
    cy.acceptCookies()
  })

  it.only('should show the admin username on the top bar when logged in', () => {
    cy.visit('/')
    cy.get('.dropdown-toggle').contains('Inloggen')
    cy.login()
    cy.get('.dropdown-toggle').contains('mdv admin')
  })
})
