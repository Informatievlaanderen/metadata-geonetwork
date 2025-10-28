export {};

declare global {
  namespace Cypress {
    interface Chainable {
      loginAdmin(): Chainable<void>;
      loginEditor(): Chainable<void>;
      loginReviewer(): Chainable<void>;
      login(username, password): Chainable<void>;
      logout(): Chainable<void>;
      acceptCookies(): Chainable<void>;
      importXml(fixtureFile): Chainable<void>;
      deleteRecord(uuid): Chainable<void>;
      validateRecord(uuid): Chainable<void>;
    }
  }
}
