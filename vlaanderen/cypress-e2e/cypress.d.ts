export {};

declare global {
  namespace Cypress {
    interface Chainable {
      acceptCookies(): Chainable<void>;
      api(method: string, url: string, user: Object, acceptedStatusCodes: number[]): Chainable<void>;
      deleteRecord(uuid): Chainable<void>;
      importXml(fixtureFile): Chainable<void>;
      login(username, password): Chainable<void>;
      loginAdmin(): Chainable<void>;
      loginEditor(): Chainable<void>;
      loginReviewer(): Chainable<void>;
      recordCount(draft: boolean, template: boolean): Chainable<number>;
      logout(): Chainable<void>;
      deleteTemplates(): Chainable<void>;
      ensureReindex(): Chainable<void>;
      ensureTemplates(): Chainable<void>;
      isIndexing(): Chainable<void>;
      reindexAll(): Chainable<void>;
      reloadTemplates(schema): Chainable<void>;
      validateRecord(uuid): Chainable<void>;
      waitUntilNotIndexing(maxAttempts, delayMs): Chainable<void>;
    }
  }
}
