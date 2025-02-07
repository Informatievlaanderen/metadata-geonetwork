describe('Idempotent editor save', () => {

  const uuid = 'b55d73cc-73b1-441e-a769-5d1b3df9f9a5'

  beforeEach(() => {
    // first login
    cy.visit('/')
    cy.login()
    cy.acceptCookies()
    // check the test record and delete it if it's present
    cy.request({
      method: "GET",
      url: "/srv/eng/info?type=me",
      auth: {
        username: "mdv",
        password: "admin"
      },
      headers: {
        accept: "application/json",
        "content-type": "application/json"
      },
      failOnStatusCode: false
    }).then(response => {
      cy.getCookie("XSRF-TOKEN").then(c => {
        const xsrfToken = c.value
        cy.request({
          method: "DELETE",
          url: "/srv/api/records/"+uuid,
          auth: {
            username: "mdv",
            password: "admin"
          },
          headers: {
            "X-XSRF-TOKEN": xsrfToken
          },
          failOnStatusCode: false
        }).then((response) => {
          console.log('delete response: ' + response.status)
          cy.wrap(response.status).should('be.oneOf', [404, 204])
        })
      })
    })
  })

  it('imports a known XML', () => {
    // load the import view
    cy.visit('/srv/eng/catalog.edit#/import')
    // paste the XML
    cy.get('#gn-import-mode-copypaste-radio').click()
    cy.fixture('dataset-open-nongeo.xml').then(xml => {
      cy.get('#gn-import-copypaste-textarea').invoke('val', xml)
      cy.get('#gn-import-copypaste-textarea').type(' ')
    })
    // cy.get('#gn-import-action-list-generate-radio').click()
    cy.get('#gn-import-buttons-import').click()

    cy.get('a[title="view"]').click()
    cy.acceptCookies()

    cy.url().then((url) => {
      const uuid = url.split("/").pop()
      console.log("uuid: " + uuid)

      cy.get('.gn-md-edit-btn').click()
      cy.wait(1000)
      cy.get('#gn-editor-btn-close').click()
      cy.get("h1").contains("[test-record] open non-geo (nl)").should('exist')

      cy.fixture('dataset-open-nongeo.xml').then(xml => {
        const expected = xml.toString().replace('7c2bab5c-7af1-42da-af4c-921c8615a2cd', uuid).trim()
        cy.request('/srv/api/records/' + uuid + '/formatters/xml').its('body').then(b => {
          const actual = b.toString().trim()
          console.log('expected')
          console.log(expected)
          console.log('actual')
          console.log(actual)
          console.log("==: "+(expected==actual))
          console.log("===: "+(expected===actual))
          console.log("==t: "+(expected.trim()==actual.trim()))
          console.log("==?: "+(expected.replace(/\s+/g,'')===actual.replace(/\s+/g,'')))
          cy.wrap(actual.replace(/\s+/g,'')).should('eq', expected.replace(/\s+/g,''))

        })
      })
    });
  })
})
