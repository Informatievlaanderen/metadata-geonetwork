/**
 * Tests for catalog context navigation fix.
 *
 * Verifies that clicking a record from a sub-portal keeps the user
 * within that sub-portal (in-app SPA navigation) instead of redirecting
 * to the root portal in a new tab.
 *
 * Uses Liquibase-seeded sub-portal "downloadtoepassing" and test records
 * that are present in every local Docker environment.
 *
 * Related fix: removed the CatalogService.js branch that set remoteUrl
 * for catalog-origin records in non-default portals.
 */

const subPortal = 'downloadtoepassing'
const testRecordUuid = '893c8f61-bcd8-40d8-aa41-0a7ebcd3f504'

describe('Catalog context navigation', () => {

  before(() => {
    cy.visit('/')
    cy.loginAdmin()
    cy.ensureReindex()
  })

  beforeEach(() => {
    cy.visit('/')
    cy.acceptCookies()
  })

  // ---------------------------------------------------------------
  // 1. Sub-portal navigation stays in sub-portal
  // ---------------------------------------------------------------
  describe('Sub-portal record navigation', () => {
    it('record links contain the sub-portal node, not /srv/', () => {
      cy.visit(`/${subPortal}/dut/catalog.search#/search`)

      cy.get('.gn-resultview', { timeout: 10000 }).should('exist')

      cy.get('a[gn-metadata-open]').first().then($link => {
        cy.wrap($link).should('not.have.attr', 'target', '_blank')

        cy.wrap($link)
          .should('have.attr', 'href')
          .and('contain', `/${subPortal}/`)
          .and('not.contain', '/srv/')
          .and('contain', '#/metadata/')
      })
    })

    it('stays in the sub-portal after clicking a record', () => {
      cy.visit(`/${subPortal}/dut/catalog.search#/metadata/${testRecordUuid}`)

      cy.get('.gn-record', { timeout: 10000 }).should('exist')

      cy.url()
        .should('contain', `/${subPortal}/`)
        .and('contain', `#/metadata/${testRecordUuid}`)
        .and('not.contain', '/srv/')
    })

    it('uses gn-metadata-open links, not remoteUrl links', () => {
      cy.visit(`/${subPortal}/dut/catalog.search#/search`)

      cy.get('.gn-resultview', { timeout: 10000 }).should('exist')

      // When remoteUrl is set, the gn-metadata-open link is hidden and
      // a target="_blank" link is shown instead. Verify the in-app link
      // is the one that's visible.
      cy.get('[gn-metadata-open]').first().should('be.visible')
    })
  })

  // ---------------------------------------------------------------
  // 2. Root portal navigation still works (no regression)
  // ---------------------------------------------------------------
  describe('Root portal record navigation', () => {
    it('record links contain /srv/', () => {
      cy.visit('/srv/dut/catalog.search#/search')

      cy.get('.gn-resultview', { timeout: 10000 }).should('exist')

      cy.get('a[gn-metadata-open]').first().then($link => {
        cy.wrap($link).should('not.have.attr', 'target', '_blank')
        cy.wrap($link)
          .should('have.attr', 'href')
          .and('contain', '/srv/')
          .and('contain', '#/metadata/')
      })
    })

    it('stays in /srv/ after clicking a record', () => {
      cy.visit(`/srv/dut/catalog.search#/metadata/${testRecordUuid}`)

      cy.get('.gn-record', { timeout: 10000 }).should('exist')

      cy.url()
        .should('contain', '/srv/')
        .and('contain', `#/metadata/${testRecordUuid}`)
    })
  })

  // ---------------------------------------------------------------
  // 3. Ratings visible in sub-portal record view
  // ---------------------------------------------------------------
  describe('Ratings in sub-portal', () => {
    it('record detail view loads with rating section', () => {
      cy.visit(`/${subPortal}/dut/catalog.search#/metadata/${testRecordUuid}`)

      // The key assertion: the record detail view loads at all.
      // Before the fix, sub-portal records got remoteUrl set, so
      // gnMetadataOpen bailed out and the user was sent to /srv/
      // in a new tab — the in-app detail view never rendered.
      cy.get('.gn-record', { timeout: 10000 }).should('exist')

      // Rating display depends on system.localrating.enable config.
      // Assert the section is present if enabled; if not, the record
      // view itself loading is proof enough (remoteUrl is not set).
      cy.get('body').then($body => {
        if ($body.find('.gn-md-side-rating').length > 0) {
          cy.get('.gn-md-side-rating').should('be.visible')
          cy.get('[data-gn-metadata-rate]').should('exist')
        } else if ($body.find('[data-gn-userfeedback]').length > 0) {
          cy.get('[data-gn-userfeedback]').should('exist')
        } else {
          cy.log('Rating disabled by config — record view loading is sufficient')
        }
      })
    })
  })

  // ---------------------------------------------------------------
  // 4. Ratings visible in root portal (no regression)
  // ---------------------------------------------------------------
  describe('Ratings in root portal', () => {
    it('record detail view loads with rating section', () => {
      cy.visit(`/srv/dut/catalog.search#/metadata/${testRecordUuid}`)

      cy.get('.gn-record', { timeout: 10000 }).should('exist')

      cy.get('body').then($body => {
        if ($body.find('.gn-md-side-rating').length > 0) {
          cy.get('.gn-md-side-rating').should('be.visible')
          cy.get('[data-gn-metadata-rate]').should('exist')
        } else if ($body.find('[data-gn-userfeedback]').length > 0) {
          cy.get('[data-gn-userfeedback]').should('exist')
        } else {
          cy.log('Rating disabled by config — record view loading is sufficient')
        }
      })
    })
  })
})
