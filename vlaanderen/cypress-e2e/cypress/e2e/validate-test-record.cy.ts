describe('Validate test record', () => {

  it('open the editor and validates the record', () => {
    // first login
    cy.visit('/')
    cy.acceptCookies()
    cy.login()
    // validate known test record(s)
    var uuid = 'b6934c23-bffa-40de-ac34-7f1f6e1dbdf1'
    console.log('getting cookies...');
    cy.getCookie('XSRF-TOKEN')
      .should('have.property', 'value')
      .then((xsrfToken) => {
        cy.request({
          method: 'PUT',
          url: `/srv/api/records/validate?uuids=${uuid}&approved=true`,
          headers: {
            'X-XSRF-TOKEN': xsrfToken,
            'Accept': 'application/json'
          }
        })
          .then((response) => {
            expect(response.body).to.have.property('metadata');
            expect(response.body.metadata).to.have.lengthOf(1);
            expect(response.body).to.have.property('numberOfRecords', 1);
            expect(response.body).to.have.property('numberOfRecordsWithErrors', 0);
          })
      });
  })
})
