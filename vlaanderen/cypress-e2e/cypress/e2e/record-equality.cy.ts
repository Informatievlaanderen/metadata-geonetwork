describe('Idempotent editor save', () => {

  it('equals a known xml', () => {
    // first login
    cy.visit('/')
    cy.login()
    cy.acceptCookies()

    const uuid = '57a3faba-7d59-475e-b1c9-d8b64a5a307a';
    cy.fixture('dataset-open-nongeo.xml').then(xml => {
      // const expected = xml.toString().replace('6e3965dc-5495-4552-94d6-37fc19a53c59', uuid)
      const expected = xml.toString()
        .replace('6e3965dc-5495-4552-94d6-37fc19a53c59', uuid).trim();
      cy.request({
        url: '/srv/api/records/' + uuid + '/formatters/xml',
        headers: {
          'Content-Type': 'application/xml'
        }
      }).its('body').then(value =>{
        const actual = value.toString().trim();
        cy.wrap(actual).should('eq', expected)
      })

    });

  })
})
