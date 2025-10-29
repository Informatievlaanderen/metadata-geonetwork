// Import commands.js using ES2015 syntax:
import './commands'

// this runs before _all_ tests
before(() => {
  // cy.log('I run before every test in every spec file!!!!!!')
  // // start by loading root
  // cy.visit('/')
  // // accept the cookie popup; not doing anything test related with this so might as well get it out of the way
  // cy.acceptCookies()

  cy.log('BEFORE ALL')
  cy.visit('/')
  cy.reindexAll()
  cy.waitUntilNotIndexing(10, 500)
  // cy.reloadTemplates('dcat-ap')
  // cy.reloadTemplates('iso19139')
  // cy.reloadTemplates('iso19110')
})

beforeEach(() => {
  // root-level hook
  // runs before every test block
})

afterEach(() => {
  // runs after each test block
})

after(() => {
  // runs once all tests are done
})
