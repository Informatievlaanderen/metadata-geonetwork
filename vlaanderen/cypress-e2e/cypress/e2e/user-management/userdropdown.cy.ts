describe('User dropdown', () => {

  beforeEach('passes', () => {
    cy.visit(`/`)
    cy.acceptCookies()
    // should be able to run this function twice without crashing
    cy.acceptCookies()
  })

  it('shows admin user info when logged in', () => {
    cy.loginAdmin()
    cy.visit('/')
    cy.get('.aiv-login-wrapper').click()
    cy.get('.logged-in-container[data-ng-show="authenticated"] ul.aiv-signin-dropdown').within(() => {
      cy.get('li:nth-child(3)').should('have.text', 'Gebruikersnaam')
      cy.get('li:nth-child(4)').should('contain.text', 'mdv admin')
    })
  })

  it('shows editor user info when logged in', () => {
    cy.loginEditor()
    cy.visit('/')
    cy.get('.aiv-login-wrapper').click()
    cy.get('.logged-in-container[data-ng-show="authenticated"] ul.aiv-signin-dropdown').within(() => {
      cy.get('li:nth-child(3)').should('have.text', 'Gebruikersnaam')
      cy.get('li:nth-child(4)').should('contain.text', 'Edith Dor')
      cy.get('li:nth-child(5)').should('have.text', 'Gebruikersprofiel')
      cy.get('li:nth-child(6)').should('contain.text', 'Editor')
      cy.get('li:nth-child(7)').should('have.text', 'Groep')
      cy.get('li:nth-child(8)').should('contain.text', 'Digitaal Vlaanderen')
    })
  })

  it('allows logging out', () => {
    cy.loginAdmin()
    cy.logout()
    cy.get('div.logged-in-container span.aiv-sign-in')
      .contains("Inloggen")
      .should('exist')
  })

})
