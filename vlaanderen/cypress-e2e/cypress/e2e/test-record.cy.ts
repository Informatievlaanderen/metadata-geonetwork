describe('Test-record tests', () => {
  it('Loads a specific test record and displays the right content', () => {
    // load test record 1 view
    cy.visit('/srv/dut/catalog.search#/metadata/b6934c23-bffa-40de-ac34-7f1f6e1dbdf1');
    cy.contains('Accept').click();
    // check title
    cy.get('.gn-record h1').invoke('text').should('contains', 'Voorlopig referentiebestand gemeentegrenzen');
    // check abstract content
    cy.get('p[data-ng-bind-html="(mdView.current.record.resourceAbstract) | linky | newlines"]').invoke('text').should('contains', 'Het Voorlopig Referentiebestand Gemeentegrenzen bevat informatie over de afbakeningen van het grondgebied van de bestuurlijke eenheden');
  });

  it('Loads the XML view and displays the expected content', () => {
    cy.request('/srv/api/records/b6934c23-bffa-40de-ac34-7f1f6e1dbdf1/formatters/xml').its('body').should('include', '<gco:CharacterString>b6934c23-bffa-40de-ac34-7f1f6e1dbdf1</gco:CharacterString>')
  });
})
