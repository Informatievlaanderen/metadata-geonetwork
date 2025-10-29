describe('Liquibase test record', () => {

  beforeEach(() => {
    cy.loginAdmin()
  })

  it('displays the right content', () => {
    // load test record 1 view
    cy.visit('/srv/dut/catalog.search#/metadata/b6934c23-bffa-40de-ac34-7f1f6e1dbdf1')
    cy.acceptCookies()
    // check title
    cy.get('.gn-record h1').invoke('text').should('contains', 'Voorlopig referentiebestand gemeentegrenzen')
    // check abstract content
    cy.get('p[data-ng-bind-html="(mdView.current.record.resourceAbstract) | linky | newlines"]').invoke('text').should('contains', 'Het Voorlopig Referentiebestand Gemeentegrenzen bevat informatie over de afbakeningen van het grondgebied van de bestuurlijke eenheden')
  })

  it('is exported correctly to XML', () => {
    cy.request('/srv/api/records/b6934c23-bffa-40de-ac34-7f1f6e1dbdf1/formatters/xml').its('body').should('include', '<gco:CharacterString>b6934c23-bffa-40de-ac34-7f1f6e1dbdf1</gco:CharacterString>')
  })
})
