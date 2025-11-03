// ***********************************************
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

type User = {
  username: string;
  password: string;
};

let testUsers = {
  admin: {
    username: 'mdv',
    password: 'admin'
  },
  editor: {
    username: 'editor',
    password: 'Editor$1'
  },
  reviewer: {
    username: 'reviewer',
    password: 'Reviewer$1'
  }
}

/**
 * Can be called multiple times, ensures only one reindex occurs. Handy when not needing a reindex at all.
 */
let reindexWasEnsured = false
Cypress.Commands.add('ensureReindex', () => {
  if(!reindexWasEnsured) {
    reindexWasEnsured = true
    cy.visit('/')
    cy.loginAdmin()
    cy.reindexAll()
    cy.waitUntilNotIndexing(10, 1000)
  }
});

let templatesWereEnsured = false
Cypress.Commands.add('ensureTemplates', () => {
  if(!templatesWereEnsured) {
    templatesWereEnsured = true
    cy.visit('/')
    cy.loginAdmin()
    cy.deleteTemplates()
    cy.reloadTemplates('dcat-ap')
    cy.reloadTemplates('iso19139')
    cy.reloadTemplates('iso19110')
  }
});

/**
 * Perform a login through the UI.
 */
Cypress.Commands.add('loginAdmin', () => {
  cy.login(testUsers.admin.username, testUsers.admin.password)
});

Cypress.Commands.add('loginEditor', () => {
  cy.login(testUsers.editor.username, testUsers.editor.password)
});
Cypress.Commands.add('loginReviewer', () => {
  cy.login(testUsers.reviewer.username, testUsers.reviewer.password)
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

Cypress.Commands.add('reindexAll', () => {
  cy.api("PUT", "/srv/api/site/index?reset=true", testUsers.admin, [200])
})

Cypress.Commands.add('reloadTemplates', (schema) => {
  cy.api("PUT", "/srv/api/records/templates?schema=" + schema, testUsers.admin, [201])
})

Cypress.Commands.add('api', (method: string, url: string, user: User, acceptedStatusCodes: number[]) => {
  cy.getCookie('XSRF-TOKEN')
    .should('have.property', 'value')
    .then((xsrfToken) => {
      cy.request({
        method: method,
        url: url,
        auth: {
          username: user.username,
          password: user.password
        },
        headers: {
          "X-XSRF-TOKEN": xsrfToken,
          'Accept': 'application/json'
        },
        failOnStatusCode: false
      }).then((response) => {
        console.log('api response (' + url + '): ' + response.status)
        cy.wrap(response.status).should('be.oneOf', acceptedStatusCodes)
      })
    });
})

Cypress.Commands.add('deleteTemplates', () => {
  cy.getCookie('XSRF-TOKEN')
    .should('have.property', 'value')
    .then((xsrfToken) => {
      cy.request({
        method: 'POST',
        url: '/srv/api/search/records/_search',
        // auth: {
        //   username: testUsers.admin.username,
        //   password: testUsers.admin.password
        // },
        headers: {
          "X-XSRF-TOKEN": xsrfToken,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: {
          "size": 10000,
          "query": {
            "match": {
              "isTemplate": "y"
            }
          },
          "_source": [
            "uuid"
          ]
        },
        failOnStatusCode: true
      }).then((response) => {
        cy.log('templateUuids response: ' + response.status)
        cy.log(response.body.hits)
        cy.wrap(response.body.hits.hits).each((hit) => {
          let uuid = hit["_source"].uuid;
          cy.log(uuid)
          cy.deleteRecord(uuid)
        })
      })
    });
})

/**
 * This command allows to wait until the indexing process has completed.
 */
Cypress.Commands.add('waitUntilNotIndexing', (maxAttempts, delayMs) => {
  let action = () => cy.request({
    method: 'GET',
    url: '/srv/api/site/indexing',
    headers: {
      'Accept': 'application/json',
    },
    failOnStatusCode: true
  }).then((response) => {
    let indexing = response.body as boolean
    cy.wrap(!indexing)
  })

  let chain = action()
  for (let i = 0; i < maxAttempts; i++) {
    chain = chain.then((foundMatch) => {
      if (!foundMatch) {
        cy.wait(delayMs);
        return action();
      }
    });
  }
  chain.then((foundMatch) => assert.isTrue(foundMatch));
  cy.wait(1000)
})
