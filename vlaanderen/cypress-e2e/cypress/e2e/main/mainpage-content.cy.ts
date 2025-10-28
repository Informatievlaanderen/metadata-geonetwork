describe('Home page', () => {
  it('is loading when navigating to root', () => {
    cy.visit('/')
    cy.acceptCookies()
    cy.url().should('contains', 'srv/dut/catalog.search#/home')
  })
})
