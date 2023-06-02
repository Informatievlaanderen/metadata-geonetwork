describe('Mainpage tests', () => {
  it('Loads the main page and navigates to the right url', () => {
    cy.visit('/')
    cy.contains('Accept').click()
    cy.url().should('contains', 'srv/dut/catalog.search#/home')
  })
})
