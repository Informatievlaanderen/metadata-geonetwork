describe('Validation of test record', () => {

  it('can be done through the API', () => {
    // first login
    cy.visit('/')
    cy.loginAdmin()
    // validate known test record(s)
    var uuid = 'b6934c23-bffa-40de-ac34-7f1f6e1dbdf1'
    console.log('getting cookies...');
    cy.getCookie('XSRF-TOKEN')
      .should('have.property', 'value')
      .then((xsrfToken) => {
        cy.request({
          method: 'PUT',
          url: `/srv/api/records/validate?uuids=${uuid}&approved=false`,
          headers: {
            'X-XSRF-TOKEN': xsrfToken,
            'Accept': 'application/json'
          }
        })
          .then((response) => {
            expect(response.body).to.have.property('numberOfRecords', 1);
            expect(response.body).to.have.property('numberOfRecordsWithErrors', 0);
            expect(response.body).to.have.property('metadataErrors');
            expect(response.body.metadataErrors).to.be.empty;
          })
      });
  })
})
