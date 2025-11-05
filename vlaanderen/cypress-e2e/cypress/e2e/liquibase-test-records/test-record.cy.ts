describe('Liquibase test record', () => {

  beforeEach(() => {
    cy.visit('/')
    cy.loginAdmin()
    cy.ensureReindex()
  })

  let uuid = 'b6934c23-bffa-40de-ac34-7f1f6e1dbdf1'

  it.only('displays the right content', () => {
    cy.visit('/')
    cy.acceptCookies()
    // load test record 1 view
    cy.visit(`/srv/dut/catalog.search#/metadata/${uuid}`)
    // check title
    cy.get('.gn-record h1').invoke('text').should('contains', 'Voorlopig referentiebestand gemeentegrenzen')
    // check abstract content
    cy.get('p[data-ng-bind-html="(mdView.current.record.resourceAbstract) | linky | newlines"]').invoke('text').should('contains', 'Het Voorlopig Referentiebestand Gemeentegrenzen bevat informatie over de afbakeningen van het grondgebied van de bestuurlijke eenheden')
  })

  it('is exported correctly to XML', () => {
    cy.request(`/srv/api/records/${uuid}/formatters/xml`).its('body').should('include', `<gco:CharacterString>${uuid}</gco:CharacterString>`)
  })
})
