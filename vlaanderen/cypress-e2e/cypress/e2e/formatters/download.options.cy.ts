describe('Download options', () => {

  beforeEach(() => {
    // set up
    cy.visit('/')
    cy.acceptCookies()
  })

  let options = {
    zip: 'Exporteer (ZIP)',
    pdf: 'Exporteer (PDF)',
    xml: 'Exporteer (XML)',
    rdf: 'Exporteer (RDF/XML)'
  }

  let tests = [
    {
      uuid: "43f9e1ef-4458-4da3-a6fe-3f325c92f264",
      type: "iso service",
      options: [options.zip, options.pdf, options.xml, options.rdf]
    },
    {
      uuid: "b6934c23-bffa-40de-ac34-7f1f6e1dbdf1",
      type: "iso dataset",
      options: [options.zip, options.pdf, options.xml, options.rdf]
    },
    {
      uuid: "893c8f61-bcd8-40d8-aa41-0a7ebcd3f504",
      type: "dcat dataset",
      options: [options.zip, options.pdf, options.xml]
    },
    {
      uuid: "bb4c9661-b40b-4393-992a-0b4c1f7ed901",
      type: "dcat service",
      options: [options.zip, options.pdf, options.xml]
    }
  ]

  tests.forEach((test) => {
    it('show correctly for ' + test.type, () => {
      // load the create record view
      cy.visit(`/srv/dut/catalog.search#/metadata/${test.uuid}`)
      cy.get('button').contains('Download bestand').click()

      cy.get('div.md-actions.open ul.dropdown-menu').within(() => {
        test.options.forEach((option) => {
          cy.get('li').contains(option).should('be.visible')
        })
        cy.get('li').filter(':visible').should('have.length', test.options.length+1)
      })
    })
  })

})
