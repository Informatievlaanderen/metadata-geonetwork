describe('Testing the login functionality', () => {

  it('Should show the admin username on the top bar when logged in', () => {
    cy.visit('/')
    cy.get('.dropdown-toggle').contains('Inloggen')
    cy.loginAdmin()
    cy.get('.dropdown-toggle').contains('mdv admin')
  })
})
