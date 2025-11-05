describe('Home page', () => {

  beforeEach(() => {
    cy.visit('/')
    cy.acceptCookies()
  })

  it('is loading when navigating to root', () => {
    cy.url().should('contains', 'srv/dut/catalog.search#/home')
  })

  it('can switch ui language by clicking the bottom buttons', () => {
    cy.get('a.aiv-language-item').contains('en').click()
    cy.url().should('contains', 'srv/eng/catalog.search#/home')
  })
})
