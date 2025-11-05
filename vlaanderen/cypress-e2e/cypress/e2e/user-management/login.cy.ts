describe('Login dropdown', () => {

  it('shows the admin username on the top bar when logged in', () => {
    cy.loginAdmin()
    cy.visit('/')
    cy.get('.aiv-login-user-info').contains('Admin')
  })

  it('can switch between roles', () => {
    cy.loginEditor()
    cy.visit('/')
    cy.get('.aiv-login-user-info').contains('Editor')
    cy.logout()
    cy.loginAdmin()
    cy.visit('/')
    cy.get('.aiv-login-user-info').contains('Admin')
  })
})
