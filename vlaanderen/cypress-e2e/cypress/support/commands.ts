// ***********************************************
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

/**
 * Perform a login through the UI.
 */
Cypress.Commands.add('loginAdmin', () => {
  cy.login('mdv', 'admin')
});

Cypress.Commands.add('loginEditor', () => {
  cy.login('editor', 'Editor$1')
});
Cypress.Commands.add('loginReviewer', () => {
  cy.login('reviewer', 'Reviewer$1')
});

Cypress.Commands.add('login', (username, password) => {
  cy.log('logging IN! ' + username + ' ' + password)
  cy.log('login (user,pass)')
  cy.session([username, password], () => {
    cy.visit('/')
    cy.acceptCookies()
    cy.get('.logged-in-container:not(.ng-hide)').click();
    cy.get('#inputUsername').type(username);
    cy.get('#inputPassword').type(password);
    cy.get(".signin-dropdown > .dropdown-menu [type='submit']").click();
  }, {
    validate() {
      cy.request({
        method: 'GET',
        headers: {'accept': 'application/json'},
        url: '/srv/api/me'
      }).its('body').then(result => {
        expect(expect(Number.isInteger(+result.id), 'input should be an integer').to.eq(true))
      })
    }
  })
});

Cypress.Commands.add('logout', () => {
  cy.visit('/')
  cy.get('.aiv-login-wrapper').click()
  cy.get('a[title="Uitloggen"]').click()
  cy.get('div.logged-in-container span.aiv-sign-in')
})

/**
 * Accept cookies, if the button is present. Should be conditional, otherwise cypress fails on not finding the button,
 * which happens if the session has already accepted the cookie in a previous test.
 */
Cypress.Commands.add('acceptCookies', () => {
  cy.get('button[data-ng-click="acceptCookies()"]').click({force: true})
});

Cypress.Commands.add('importXml', (fixtureFile) => {
  // load the import view
  cy.visit('/srv/eng/catalog.edit#/import')
  // paste the XML
  cy.get('#gn-import-mode-copypaste-radio').click()
  cy.fixture(fixtureFile).then(xml => {
    cy.get('#gn-import-copypaste-textarea').invoke('val', xml)
    cy.get('#gn-import-copypaste-textarea').type(' ')
  })
  // cy.get('#gn-import-action-list-generate-radio').click()
  cy.get('#gn-import-buttons-import').click()

  cy.get('a[title="view"]').click()
})

Cypress.Commands.add('validateRecord', (uuid) => {
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

Cypress.Commands.add('deleteRecord', (uuid) => {
  cy.getCookie('XSRF-TOKEN')
    .should('have.property', 'value')
    .then((xsrfToken) => {
      cy.request({
        method: "DELETE",
        url: "/srv/api/records/" + uuid,
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
    });
})
