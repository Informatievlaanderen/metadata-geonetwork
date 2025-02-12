# Changelog
All notable changes to this project will be documented in this file. These changes are specific to Vlaanderen, important [core-geonetwork](https://github.com/geonetwork/core-geonetwork) changes are linked or embedded.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [8.2.3] - 2024-11-05

### vlaanderen
- Keeping track of `doelgroep` values returned by ACM/IDM. Groups such as EA now allowed - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/39330)
- GDI-VL-Conform keyword now added based on correct prerequisites - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/39553)
- Dataset editor improvements - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/39437)
- Fix harvest of single `rdf:RDF` documents - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/39663)
- Workflow fix for publishing draft copies - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/39626)
- Changed SMTP `from` address to `no_reply@digitaal.vlaanderen.be` - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/39786)
- Added `/groups/preallocate` endpoint and admin tool that integrates with the Organisatieregister - [pr](https://agiv.visualstudio.com/Metadata/_git/0a154993-bcec-4021-98e4-034a6161db36/pullrequest/39624)
- Displaying distributions for extra protocols on default view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/40144) 
- Fixed potential nullPointer when sending mails after harvest - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/40194)
- Fix for multiple ISO `gmd:deliveryPoint` elements - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetworkMicroservices/pullrequest/40145)

### core
- Fixing whitespace issue for specific css class - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/39432) / [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/39608) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/8398)
- Merged 4.4.5-0 - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/39793) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/8184)
- **Hotfix** for `json-smart` dependency build issue - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/8654)


## [8.2.2] - 2024-09-27

### vlaanderen
- Data.gov.be keyword fixes: uniqueness and prevent erroneous ISO category override - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/38386) / [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/38390)
- Enabled `gmd:onLine` elements in iso19139 editor - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/39400)


## [8.2.1] - 2024-07-17

### vlaanderen
- Cleanup of DCAT2 plugin to make it available for general use - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/36672)
- Hotfix: broken full view editor due to duplicate rdf file - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35995)

### core-geonetwork
- Additional fixes for double translation bug - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/36762) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/8209)


## [8.2.0] - 2024-05-27

### vlaanderen
- Record view / Service metadata / Move resource constraints to the legal section - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35579)
- Fixed duplicated labels in full iso19139 view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35542)
- DCAT / ConformsTo- dct:Standard class is missing dct:identifier - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataDcatAp/pullrequest/35553)
- Translation improvements - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35547) / [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35723)
- Facet label fix - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35549)
- Profile and standard facets visible for anonymous users - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35644)
- Catching frontend errors - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35706)
- Editor optimisation, not displaying large amount of tables - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35571)
- Fix for ghost copies in the editor board - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35753)
- Not displaying draft copy status in search and facets - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35774)

### core-geonetwork
- Log / Remove mail debug information - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35670) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/8043)
- Added groupOwner check while testing for permissions in Elasticsearch - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35160) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7980)
- Merged 4.4.5-SNAPSHOT, Elasticsearch 8 upgrade  - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/33251)
- Fixed broken link to draft copy editor in search results - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35546) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/8031)
- Record view / Focus on organisation fix - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35646) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/8040)
- Multilingual support for `getIndexField` - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35661) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/8042)
- Added groupOwner check while testing for permissions in Elasticsearch - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35160) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7980)


## [8.1.18] - 2024-04-30

### vlaanderen
- Added missing `/id/GDI-Vlaanderen-Vlaamse-Administratieve-Eenheden` file - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/34937)
- Editor now correctly handling large forms - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35087) / [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35091) / [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35203)
- ACM/IDM integration now handles parallel requests - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35168) 
- Handling invalid emails correctly - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35175)
- Removed incorrect characters from harvester mail templates - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35189)
- Harvester logs now accessible through mail template - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35189)
- Now using beta environment as intended for status change mails - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35272)
- Hotfix: fresh users could not be created due to introduced transactions - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/35362)


## [8.1.17] - 2024-04-16

### vlaanderen
- CSW now uses the gml namespace instead of the gml/3.2 namespace - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/33444)
- Fixed metadatacenter reference in RDF - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetworkMicroservices/pullrequest/34567) / [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/34566)

### core-geonetwork
- Improvements in record view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/33256) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7811)


## [8.1.16] - 2024-03-01

### vlaanderen
- Bugfix for service accounts, reviewers are now also assigned editor role - [pr](https://agiv.visualstudio.com/Metadata/_git/0a154993-bcec-4021-98e4-034a6161db36/pullrequest/33201)
- Bugfix for CSW properties update request: fix gmd:dateStamps/gco:Date parsed as DateTime - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/33223)
- Enforce `gco:Date` for creation, publication, modification dates - [pr](agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/33243)
- Automated changelog generation and publication - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/33279)
- Translation fixes - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/33301)


## [R8] - 2024-02-26
- Digitaal Vlaanderen implementeert een aanzienlijke administratieve vereenvoudiging door het aantal metadata-knooppunten te reduceren en door de publicatieprocesflow te optimaliseren
    - Het metadatacenter wordt samengevoegd met Metadata Vlaanderen
    - Het traject van een metadatarecord van ontwerp tot publicatie wordt aanzienlijk gestroomlijnd
- Tegelijkertijd optimaliseert Digitaal Vlaanderen de achterliggende infrastructuur en technologie
    - De infrastructuur wordt een beheerde Kubernetes cluster (AKS) in de Azure-cloud
    - De software migreert van GeoNetwork 3.8 naar GeoNetwork 4.4, wat ons opnieuw aligneert met de laatste core versie van het Open Source Software pakket
    - De gebruikte zoekindex wordt ElasticSearch in plaats van Lucene, wat de vindbaarheid van gegevens voor eindgebruikers sterk verbetert
    - De nieuwe 'look and feel' verbetert de gebruiksvriendelijkheid van de toepassing
- Tot slot wordt Metadata Vlaanderen nog veiliger door het inloggen van eindgebruikers én API clients via het Toegangs- (ACM) en Gebruikersbeheer (IDM) van de Vlaamse overheid te regelen


## [8.1.15] - 2024-02-23

### vlaanderen
- Fix RDF output XML formatting - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetworkMicroservices/pullrequest/32889)
- Fix DCAT indexing issues - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32888)
- Add DCAT full view missing endpointURL label - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32888)
- Change default "Blade per" facet for home page - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32888)
- Implement mapping from Topic category to Data.gov themes in ISO19139 indexing - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32888)
- Change DCAT harvester behavior to transform URI into normal UUID - [pr](agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32980)
- Create `modelLicentieObject` index field to limit number of licenses in facet - [pr](agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32980)
- Added `inspire` portal - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/33102)

### core-geonetwork
- Fix srv:operatesOn indexing when dataset uuid is not last argument of URL - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32979) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7803)
 

## [8.1.14] - 2024-02-21

### vlaanderen
- Fix empty `gco:DateTime` kept by `update-fixed-info`. Now removed and `gco:nilReason` added to parent - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32717)
- Ensure correct ISO-19139 namespaces and GML version is enforced when editing a record - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32717)
- Fix "Domain" facet to include missing "Vlaamse Open data Service" - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32717)
- Fix accessRight facet for DCAT records - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32717)


## [8.1.13] 2024-02-12

### vlaanderen
- Workflow and ui fixes - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32106)
- Implemented ACM/IDM API client access - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32347)
- Settings updates - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32373)
  - Added downloadtoepassing portal
  - Set inspirevalidator to custom deployment
- Correctly link feature catalogue using gfx outputSchema - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32462)
- Fix RDF format detection not working in some cases - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32445)
- Add support for turtle format to RDF harvester - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32445)
- Remove empty intervals for `creationYear` facet - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32514)
- Made full view the default view for DCAT records - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32514)
- Fix DCAT full view missing labels - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32514)
- Add XSL transformation to add Vlaamse Open data keywords during DCAT harvesting - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32514)
- Add reference date index field for all metadata standard and add sort option in the UI - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32514)
- Fix FC template indexing error - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32514)
- Move related dataset series information to under the related object catalogs section in the metadata view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32514)
- Fix full view tab management - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32514)
- Fix FC to DS linking process - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32514)
- Create `nonOgcwxsSourceCatalog` index field to contain the source catalog information, excluding harvested metadata originating from a `OGCWXS` harvester. Instead assigning them to the local catalog - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32514)
- Implement possibility to export draft copy via CSW GetRecords operation - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32596)
- DCAT indexing fix:  - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32596)
  - Add missing `th_<thesaurus key>_tree`
  - Fix wrong usage of 2 characters lang code instead of 3 char
  - Fix empty keywords and theme 
  - Fix invalid JSON generation
- ACM/IDM production integration - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32753)
- Added disclaimer and cookie declaration to footer - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32829)

### core-geonetwork
- Additional fixes for the indexingErrorMsg translation - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32218) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7531)
- Using consistent icons in metadata creation page - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/32514) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7721)


## [8.1.12] - 2024-01-22

### vlaanderen
- Increase number of results returned for `dct:language` thesaurus picker - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31686)
- Added record purpose to default view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31883)
- Hiding keyword type in the default editor view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31895)
- Add missing accessRights information in related records response - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31922)
- Rename thesauri identifier to fit old ones - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31915)
- Update layout of Access & use constraints in metadata view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31957)
- Fix and improve distribution details in metadata view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31958)

### core-geonetwork
- Make size of returned results in `gnKeywordSelector` configurable - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31686) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7614) 
- Additional fixes for the indexingErrorMsg translation - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31912) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7531)


## [8.1.11] - 2024-01-10

### vlaanderen
- Quality section: header cleanup and added report type - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31460)
- Hiding RDF export when not applicable - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30878)
- Add `retrievable` amount to the harvester mail template - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31626)
- Date shown for sourceSteps in view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31628)
- Display series resourceConstraints as useAndAccess constraints - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31528)
- Reordered sections of dataset view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31527)
- Date instead of dateTime in ISO19110 - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31126)
- Tweaks to "add link to ..." dropdown - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31473)
- Bugfix in organisation facet, spurious whitespace - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30906)
- Correctly show processors with `Anchor` organisationNames - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31633)

### core-geonetwork
- Merged 4.4.2-SNAPSHOT - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31500)
- Fix for duplicates-check in validation of related records - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31075) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7567)
- Fix for cryptic error for ownerless harvesters - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7539)
- Improved label for vertical extent - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31519) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7604)
- Bug fix for iso19139 indexing error - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31512) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7605)
- Fix Linux specific file separator used for harvester transform option list - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31604) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7603)
  - DCAT `rdf:resource` attribute now correctly harvested by the simple URL harvester
- Displaying phone with icon - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31471) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7598)


## [8.1.10] - 2024-01-05

### vlaanderen
- Translations - [pr1](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31081) / [pr2](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31123)
- Clearing iso19110 title on duplication - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30873)
- Translations iso19110 editor - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30873)
- Footer tweaks - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31200)

### core-geonetwork
- Fixed minor UI bug when listing languages - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/31081) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7568)


## [8.1.9] - 2023-12-14

### vlaanderen
- Remove thumbnails on import - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30536)
- Header/footer improvements - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30526)
- Schematron rule for temporalExtent + translations - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30160)
- Fixed bug related to adding conform keywords on save - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30468)
- Correctly saving gmd:date in editor for quality measurements - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30832)
- Added gmd:source and the contained gmd:sourceStep objects to record view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30633)
- Add `topLevelProtocol` to index and replace "Service Protocole" with it - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30757)
- Improve slightly layout of status workflow dropdown - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30757)
- Implement fixed order for status workflow facet - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30757)
- Run INSPIRE validation after save/close - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30546)

### core-geonetwork
- Configurable icon for static pages - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30491) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7536)
- Translation of indexingErrorMsg - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30080) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7531)


## [8.1.8] - 2023-12-08

### vlaanderen
- Added custom mailing to workflow notifications - [pr1](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30315) / [pr2](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30496)
- Header/footer improvements, responsiveness - [pr](https://agiv.visualstudio.com/DefaultCollection/Metadata/_git/MetadataGeonetwork/pullrequest/29987)
- Translations - [pr1](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30481) / [pr2](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30641)
- Added GDI vlaanderen keywords at harvest of OGC services - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29983)
- Added default dateTime for processStep in editor - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30565)
- Clean display of resourceTitle in the case of multiple values - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30574)
- Tweaks to servicetype view - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/30637)


## [8.1.7] - 2023-11-23

### vlaanderen
- Dataset identifier now added for new records - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29827)
- Added "Add Geographic keyword" transformation - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29829)
- Lengthened 1089 conformance title - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29793)
- Cleaned up quality section - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29782)
- Changing group owner now disallowed - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29768)
- Added custom header and footer - [pr1](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29876) / [pr2](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29898)
- Add additional information to the index & the relation API used by the microservice during RDF DCAT2 conversion - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29880)

### core-geonetwork
- Styling fixes - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29747) / [core-pr](https://github.com/geonetwork/core-geonetwork/pull/7502)
- Merged v4.4.1 release - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29891) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7508) / [changelog-core](https://docs.geonetwork-opensource.org/4.4/overview/change-log/version-4.4.1/)
  - Add more db information to the site information page
  - Fix cookies path when deployed on root "/" context
  - Security / Jolokia update
- Added capability to validate after harvesting - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/27953) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7370)


## [8.1.6] - 2023-11-17

### vlaanderen
- Label fixes - [pr1](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/28988) / [pr2](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29360) / [pr3](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29489)
- Search options & facet label fixes - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29375)
- Index scope as topic category for iso19110 - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29215)
- Removed mdc portal, added messaging to clarify DataPublicatie group - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29525)
- Allow editing thumbnails in side panel - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29591)
- Showing usergroups in login menu - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29697)
- Implement relation API for DCAT metadata - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29671)
  - Add RDF resource URI to index for ISO-19139 and DCAT2 records
  - Add resource URI pattern configuration for CSW and geonet harvesters
  - Augment `related` object from relation API with `rdfResourceURI` & `domain`
  - Implement relation linking in DCAT2 plugin
- Editors can now edit records that were created by admins - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29714)
- gmd:LanguageCode now uses iso639-2 - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29726)

### core-geonetwork
- Modified display of draft copies - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7477) / [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29234)
- Fix `linkServiceToDataset` directive default filter on resource type - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7489)


## [8.1.5] - 2023-11-08

### vlaanderen
- Added schema plugin translations - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/28984)
- Added group owner detail to record cards - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29051)
- Tweaked workflow status labels - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29193)
- Embedded feature catalog information reintroduced - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/28306)
- Avoiding invalid record when adding data quality report - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29162)
- Handle empty lineage section in editor - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29161)
- Fixed thesaurus selection bug in editor - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29156)
- Added constraints in ISO editor - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/27995)
- Enable addition of temporal extent in editor - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29166)
- Hiding inapplicable spatial resolution for services - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29198)

### core-geonetwork
- Added Data Quality information to record view - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7469) / [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29153)
- Record view improvements - [pr-core1](https://github.com/geonetwork/core-geonetwork/pull/7473) / [pr-core2](https://github.com/geonetwork/core-geonetwork/pull/7472) / [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/29194)


## [8.1.4] - 2023-10-25

### vlaanderen
- Removed DataPublicatie portal - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/28851)
- Workflow optimisation - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/28849)


## [8.1.3] - 2023-10-24

### vlaanderen
- Added WCS-2.0.0 as OGC-WCS service type - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/28482)
- Added missing hover labels for search buttons - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/28193)
- Enabled subportals - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/28552)

### core-geonetwork
- Merged core-geonetwork 4.4.1-SNAPSHOT
- Handle empty code list values - [pr-core](https://metadata.vlaanderen.be/srv/dut/catalog.search#/metadata/f1e77b4f-a174-4e2d-9af7-fe7f548b5a5c)


## [8.1.2] - 2023-10-16

### vlaanderen
- Ordering workflow statuses in logical way - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/27923)
- Publishing draft now sets group owner correctly - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/28255)


## [8.1.1] - 2023-09-29

### vlaanderen
- Backporting lineage and legal constraints formatter - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/27955)

### core-geonetwork
- Improved handling of empty record titles - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/27607) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7362)
- Merged core-geonetwork 4.4.0-SNAPSHOT - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/27898)
  - Introducing HA capabilities, e.g., harvester modifications
- Multiple status handling - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/27969) / [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7366)
- ISO19110 improvements - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7365)


## [8.1.0] - 2023-09-26

### vlaanderen
- Backport facets and search options from old application - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/26987)
- Display groups by pair in the editor group dropdown - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/26988)
- Workflow tweaks and fixes - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/27062)
- Fixing scheduler for high availability setups - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/27084)
- Improved status information in admin panel - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/27311)
- Running replica GeoNetwork instances - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/27534)

### core
- Merged core-geonetwork 4.4.0-SNAPSHOT - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/26874)
  - Upgraded to Java 11


## [8.0.4] - 2023-09-04

### vlaanderen
- Synced translations files with Transifex nl_BE - [pr1](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/25634) / [pr2](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/26995) / [docs](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork?path=/vlaanderen/docs/translation.md&version=GBdevelop)
- Remove unused core metadata templates from ISO19139 plugin to avoid including them when loading the templates


## [8.0.3] - 2023-07-14

### vlaanderen
- Backport changes & customization made on the ISO19139 update-fixed-info.xsl & OGC Web service harvester logic
- Fix DCAT editor issues with date field
- Added capability to disable harvester scheduling - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/25303)

### core
- Record view / Contact / Move website to popup - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7220)
- Record view / Lineage & Quality section improvements - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7180)
- Record view / Display geographic identifier and description if any.  - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7221)
- Standard / ISO19139 / Indexing / Temporal range in GML 3.2.0 - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7218)
- Merged core-geonetwork 4.2.6-SNAPSHOT changes - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/25576)
  - minor fixes, including workflow
- Add cardinality for ISO19110 - [pr](https://github.com/geonetwork/core-geonetwork/pull/7182) - [pr-core](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/25115)
- Improve performance of large forms - [pr-core](https://github.com/geonetwork/docker-geonetwork/pull/107/files#diff-bed7ab158ecf2f50be93c45dd9ae77da44d0689a155d95771d091515fb6d1ba7R84-R85)
- Replace title by empty value when creating or duplicating a metadata
- Change UI config to show absolute modification in the UI instead of relative elapsed time
- Backport changes mode on the `update-info-on-duplicate.xsl` for ISO19139
- Update codelist dut label for `gmd:CI_DateTypeCode`
- Enforce values for metadataStandardName and metadataStandardVersion during edition


## [8.0.2] - 2023-06-26

### vlaanderen
- Adding download link for RDF
- Adding VL/INSPIRE conformity keywords upon validation
- Enabled 'pin as favorite' functionality

### core-geonetwork
- High availability fix, allow configuration of separate html cache directory - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24976)
- High availability fix, define schema publication dir - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/25025)
- Work in progress: high availability - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/6990)


## [8.0.1] - 2023-06-15

### vlaanderen
- Vlaanderen Geonetwork version now visible and automatically updating
- Implement DCAT-ap metadata editor - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24798)

### core-geonetwork
- Merged core-geonetwork 4.2.5-SNAPSHOT changes - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24644)
  - Minor fixes and updates
  - Font-awesome library upgrade, minor icon changes
- Fix issue in editor where reference to an element would be lost and recreated
- Fix issue where `geonet` edit element where added multiple times
- Fixed nullpointer bug in LocaleRedirects - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24802)


## [8.0.0] - 2023-06-09

### vlaanderen
- Introduced semver versioning
- Add XML view/download options - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24005)
- Added custom workflow - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/22731)
- Added liquibase versioning for database versioning, disabling Geonetwork-managed updates - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/20246)
- Cleanup of start-page "browse by" options - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/23629)
- Customised facets - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/18729)
- Customised editor view
- Introduce ACM/IDM as default authentication layer - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/21672)
- Introducing Cypress e2e testing - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24170)
- Introduce DCAT editor - [pr1](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/22851) / [pr2](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/23974)
- Introducing DCAT plugin - [pr1](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/18131) / [pr2](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/22605)
- Modified workflow with custom states
- Porting 2005/2007 schemas and enforce default - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/18689)
- Porting ISO editor - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/21740)
- Porting thesauri of previous deployment - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/18736)

### core-geonetwork
- Allow disabling the 'search map' - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7071) / [pr](https://agiv.visualstudio.com/Metadata/_workitems/edit/170315/)
- Allow disabling automatic database migration - [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/21726)
- Config / add property file overlay, setting auto hibernate on startup - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/6954)
- Copy resources to data dir - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7110) / [pr](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/23983)
- Default tab configuration - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/6986)
- Onhover mode for tooltips - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/6987)
- Removal of magic numbers in workflow labels - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7104)
- Merged **core-geonetwork 4.2.5-SNAPSHOT**
  - Index performance improved, related to thesaurus and thumbnails
- Workflow / On Cancel / Properly remove draft from index - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7101)
- Workflow improvements - [pr-core](https://github.com/geonetwork/core-geonetwork/pull/7011)


## [R7] - 27/06/2023

### Metadata-standaard & Metadata-inhoud
- Fix en migratie voorzien voor links naar INSPIRE-URL's: deze zijn gemigreerd naar http-links in plaats van https-links, op aangeven van het INSPIRE-team
- Fix en migratie voorzien voor links naar URI’s in de DCAT-metadatarecords voor ‘mdcat-properties': deze zijn gemigreerd naar https-linken in plaats van http-linken

### Metadata-beheersysteem
- Er zijn twee nieuwe nodes aangesloten op Metadata Vlaanderen: deze van het Departement Werk en Sociale Economie en deze van Departement Cultuur, Jeugd en Media
- Hoofdzakelijk bugfixing en optimalisatie van kleine features op GeoNetwork 3.8, DCAT-AP plug-in en de Zoek-facets en indexing-mechanismen

### Overzicht van alle verbeteringen sinds R6 in detail:
- Fix voorzien voor het Sjabloon voor services: de invulvelden van de ‘ServiceOperations’ en de ‘OperatesOn’ zijn terug beschikbaar in de standaard editeeromgeving
- Fix voorzien voor de datum-zoeker functionaliteit
- Fix voorzien voor het exporteren van URI’s met een spatie naar RDF-output in de GeoDCAT mapping van de voorbeeldweergaven
- Fix voorzien voor het exporteren van formaat XML naar RDF-output
- Fix voorzien voor het exporteren van de OGC-API-Features protocol naar RDF-output in de GeoDCAT-mapping
- Update van de Shacl Validator die geïntegreerd is in GeoNetwork: verbetering op de parsing, de behandeling van de ‘ranges’ en op validatie-boodschappen, vooral in het DCAT schematron
- Fix voorzien voor het toevoegen van een ‘vrije’ beperking, die niet uit de suggestielijst komt
- Fix voor de verkeerde elementnaam van `dcat:endpointURL` naar `dcat:endpointURL`
- Fix voor het indexeren van het DCAT `dct:type` element


## [R6] - 13/03/2023

### Metadata-standaard
- Geen wijzigingen

### Metadata-inhoud
- Geen wijzigingen

### Metadata-beheersysteem
- Hoofdzakelijk bugfixing en optimalisatie van kleine features op GeoNetwork 3.8, DCAT-AP plug-in en de Zoek-facets en indexing-mechanismen

### Overzicht van alle verbeteringen sinds R5 in detail:
- Toevoeging van een facet om te zoeken op ‘Protocol’ van een service
- Fix voorzien voor de validatie op de datum-velden
- Fix voorzien voor de relatieknop in de tegels Dataset en Objectencatalogus in de resultatentlijst
- Fix voorzien voor het verkeerd linken van het element ‘gmd:contact’. Het element is verwijderd van de editeer-weergave
- Toevoegen van een extra mapping voor het protocol ‘OGC-API-Feature-items’ als een ConformsTo-protocol in de GeoDCAT RDF output
- Toevoegen van ‘mdcat:Statuut’ in de sjablonen van DCAT-AP VL en Metadata-DCAT
- Toevoegen van ‘mdcat:Statuut’ in de default- en volledige weergave in de toepassing
- Fix voorzien voor het tonen van de correcte wijzigingsdatum in de (Geo)DCAT RDF-output
- Toepassen van dezelfde mapping van native DCAT-records, zoals voor de ISO-records naar GeoDCAT
- Fix voorzien voor de mapping van distributieformaten
- Fix voorzien voor het mapping van de organisatienaam in de RDF
- Fix voorzien voor het importeren van een objectencatalogus, met een nieuwe UUID.
- Fix voorzien voor WMTS harvest (GDI-Vlaanderen trefwoord 'Metadata INSPIRE-conform' is aanwezig)


## [R5] - 11/01/2023

### Metadata-standaard
- Hoofdzakelijk verbeteringen aan de GeoDCAT-AP Vl mapping van de ISO-metadatarecords naar de RDF-output
- Bugfixing in sjablonen van de overige applicatieprofielen

### Metadata-inhoud
- Aanpassing van het element ‘Formaat’ dat nu gevoed wordt door een codelijst in plaats van een vrij in te vullen tekstveld
  - Bijhorend is het distributieblok aangepakt en opgeschoond

### Metadata-beheersysteem
- Bugfixing en optimalisatie van kleine features op GeoNetwork 3.8, DCAT-AP plug-in, en de Zoek-facets en indexing-mechanismen

### Overzicht van alle verbeteringen sinds R4 in detail:
- Inloggen via de tegel ‘Vlaamse Overheid’ kan nu op basis van een Trusted Relatie met ACM/IDM
- Fix waarbij de eerste distributie kan verwijderd worden als er meerdere aanwezig zijn
- Fix op het sjabloon voor Geografische Services
- Fix op het wegschrijven van ISO-elementen richting GeoDCAT:
  - ‘categorisaties’ zoals ISO-categorie, INSPIRE-thema, GEMET-concept, MAGDA-categorie, Statuut, ServiceType en ServiceCategorie
  - ‘Spatial Coverage’, ‘Location’
  - ‘Spatial Resolution’ voor ‘Afstand (Distance)’
  - Relatie ‘Dataservice’ > ‘Dataset’ (OperatesOn)
  - ‘Licenses & Rights’
- Met extra default ‘dct:rights statement’ als er geen relatie tussen een dataset-distributie en een service record bestaat
  - ‘versionDate’
  - Fix op dubbel voorkomen van ‘rightsHolder’
  - Fix op dubbel voorkomen van ‘Keywords’
  - Versie toegevoegd aan de ConformsTo elementen voor de gebruikte applicatieprofielen
  - CSW werd foutief als Dataset i.p.v. als Dataservice gecatalogeerd in GeoDCAT
- Fix op verschillende elementen, codelijsten en thesauri die een Nederlandstalige vertaling misten (bv: Codelijst Organisatietypes in DCAT-sjablonen)
- Fix in de doorvertaling van metadata naar de relation API
- Bijwerkingen van de SHACL-validatie toegepast in de validaties in GeoNetwork, zowel voor de ISO- als de DCAT-profielen
- Fix in het root element van native aangemaakte records
- Update van de Header & Footer
- Fix van de e-mails die worden uitgestuurd
  - Ook de trigger vanuit het harvesting-proces
- Fix in de harvest logging
- Aanmaak van ‘formatters’ zodat de pagina’s van Toegangs-en gebruiksvoorwaarden en Bewerkingen apart te bereiken zijn met een URL vanuit andere toepassingen
- Oplossing om met ‘blanc nodes’ om te gaan bij harvesten van DCAT-feeds
- Verbeteren van de performantie
  - Door verbeteringen in de RDF-export
  - Door verbeteringen in de relation API
- Fix in de edit-view waar bepaalde elementen in de DCAT-sjablonen nog ontbraken in de volledige weergave
- Fix Licentie Picker
- Fix harvester issues met DCAT-feed van Stad Antwerpen
- Voorzien van facets voor
  - Protocol
  - Domein
  - IsOpen
  - IsGeo
    - Met bijhorende migraties op metadata-inhoud van native aangemaakte records, waar nodig
- Fix vCard-issue in de UI
- Fix op het bewaren van een trefwoord uit de GDI-Vlaanderen thesaurus
- Onderzoek naar TSL/SSL encryptie
- Fix van een XML-schema fout
- Onderzoek op te strenge INSPIRE-validatie op de gmd:useLimitation
- Logica onderzoeken en uitschrijven waarom bepaalde datasets die bedoeld zijn als ‘Publiek’ toch als ‘Niet-publiek’ worden gepubliceerd >> bepaalde partijen al gecontacteerd om dit te corrigeren in hun metadata
- Fix op de UI in styling waar lange URL’s ervoor zorgden dat die bovenop het rechter zijpaneel terecht kwamen


## [R4] - 20/06/2022

### Metadata-standaard
- Hoofdzakelijk verbeteringen aan de GeoDCAT-AP Vl mapping van de ISO-metadatarecords naar de RDF-output
- Bugfixing in sjablonen van de overige applicatieprofielen, waar nodig

### Metadata-inhoud
- Aanpassing van alle vormen van de organisatienaam van 'agentschap Informatie Vlaanderen' naar 'agentschap Digitaal Vlaanderen'

### Metadata-beheersysteem
- Bugfixing en optimaliseren van kleine features op GeoNetwork 3.8, de DCAT-AP plug-in, en de Zoek-facets en indexing-mechanismen

### Overzicht van alle verbeteringen sinds R3 in detail (in chronologische volgorde)
- Fix waar voorbeeldweergaven niet konden worden opgeladen of verwijderd
- Fix crash bij de RDF-export van ISO-metadatarecords met meerdere objectencatalogi
- Changelog voorzien per omgeving (DEV, BETA, PROD)
- Toevoegen mapping van 'gmd:EX_GeographicBoundingBox' naar 'dct:spatial/dcat:bbox'
- Fix verkeerde 'SpatialRepresentationType URL' voor 'adms:representationTechnique'
- Enkel 'gmd:MD_LegalConstraints' and 'gmd:MD_SecurityConstraints' mappen naar 'dct:rights'
- Correct gebruik maken van de oorspronkelijke dataset identificator (UUID) en URI als deze aanwezig zijn en de correcte syntax gebruiken
- Fix 'dct:spatial' GML-encoding
- Update 'dcat:Catalog contact' en 'publisher' informatie
- Mapping van het originele metadatarecord (HTML-view weergave) naar 'mdcat:landingpageVoorBronMetadata' in plaats van naar de parent property 'dcat:landingPage'
- Toevoegen mapping voor 'OGC:OGC-API-Features-landingpage' en 'OGC:OGC-API-Features-items protocols'
- Toevoegen van protocol mapping voor services in het element 'conformsTo' gebaseerd op het distributie-element 'gmd:protocol'
- Fix om niet te dupliceren van de mapping waar de overdracht niet via de download protocols gebeurt ('WWW:DOWNLOAD-1.0-ftp—download', 'WWW:DOWNLOAD-1.0-http—download', of 'LINK download-store')
- Toevoeging mapping van de 'OGC:OGC-API-Features protocols' in de dataset-distributies
- Fix ontbrekende referentie naar de 'dcat:CatalogRecord', 'dcat:Dataset' en 'dcat:DataService' in de RDF-output bij exporteren via the user interface ("/dut/rdf.metadata.get" API)
- Verwijderen van de maximum kardinaliteit van de validatieregel voor het element 'statuut' voor 'DCAT-AP Vl'
- Toevoegen van via de admin settings te configureren organisatie e-mail en URL van de catalogus
- Fix niet-editeerbaar concept 'dct:rightsHolder/dct:type'
- Fix Dataset en DataService geïndexeerd onder 'standardName'
- Fix van het soms lege record onderdeel in de 'Metadata DCAT' view
- Fix van het soms lege 'Standard name' en 'description' in de 'catalog record' van geharveste metadata
- Fix gedupliceerde 'amds:identifier' in de RDF-output van bepaalde DCAT-native aangemaakte records
- Fix zodat het distributie licentie-blok in de DCAT-sjablonen verwijderd kan worden
- Toevoegen van de GeoNetwork homepage link aan 'dcat:Catalog/foaf:homepage/foaf:Document/@rdf:about attribute'
- Aanmaken van 'dct:creator' van 'dcat:CatalogRecord/adms:identifier' dynamisch gebaseerd op de gebruikte node
- Aanpassen van 'dcat:landingPage' naar 'mdcat:landingpageVoorBronMetadata'
- Fix tikfout in licentietype
- Fix 'hard line returns' in bepaalde licentie-beschrijvingen
- Verplaatsen van alle 'element-namespaces' naar het 'root-element'
- Fix character encoding in de hydra paging URL's query parameter
- Fix van de niet-editeerbare service 'dct:license/dct:LicenseDocument/dct:type'-thesaurus value
- Toevoegen van de mapping van 'status progress code' naar 'mdcat:status(sub-property of adms:status)'
- Toevoegen van de mapping van trefwoorden naar de subproperties van dct:subject:
  - http://vocab.belgif.be/auth/datatheme => `dcat:theme`
  - https://inspire.ec.europa.eu/metadata-codelist/TopicCategory => `mdcat:ISO-categorie`
  - https://inspire.ec.europa.eu/theme => `mdcat:INSPIRE-thema`
  - http://www.eionet.europa.eu/gemet => `mdcat:GEMET-concept`
  - https://data.vlaanderen.be/id/conceptscheme/MAGDA-categorie => `mdcat:MAGDA-categorie`
  - Andere trefwoorden => `dct:subject`
- Toevoegen mapping voor service types en service categorieën
- Fix tikfout in `dct:creator/@rdf:resoure` attribuutnaame
- Implementatie van caching mechanisme voor omgezette RDF-metadata voor betere performantie
- Patch voor Taxonomy indexing memory leak
- Toevoegen van de totale relation-count in het 'relation-API -antwoord' om efficiënte paginering toe te staan
- Fix ontbrekend 'dct:Location' wrapper-element
- Fix ontbrekende "root" property voor native metadata in de database
- Fix 'dcat:endpointDescription' minimum kardinaliteit
- Fix ontbrekende "*" tekens op de verplichte velden in de DCAT-sjablonen in het editeren
- Toevoegen van de + knop voor verwijderde titel en beschrijving in DataService sjabloon in de editor
- Update van het schematron met de meest recente SHACL specificatie
- Update van de Header-informatie van "agentschap Information Vlaanderen" naar "Digitaal Vlaanderen"
- Fix om dcat:distribution te verwijderen die niet het laatst zijn toegevoegd
- Implementeren van fixes op de ATOM-feed functionaliteit
- Toevoegen van dct:conformsTo in de distributie-tab in de native DCAT-sjablonen bij het editeren
- Verbeteren van de harvester notification e-mails
- Fix encoding-problemen bij het exporteren van het ISO-distributie-element naar het 'accessURL' RDF-element
- Verbeteren van de DCAT-harvester bij het omgaan met 'blank nodes'
- Toevoegen van een apart te bereiken 'Gebruiksvoorwaarden'-view in functie van de Downloadtoepassing
- Toevoegen van de mapping voor 'spatialResolution'


## [R3] - 15/03/2022

Metadata Vlaanderen integreert API’s en voorziet een uitgebreid ecosysteem aan metadata-standaarden

### Metadata-standaard: Vanaf nu kunnen alle soorten API’s beschreven worden. Het ecosysteem van metadata-standaarden in de ISO/INSPIRE- en DCAT-taal is hiervoor helemaal in GeoNetwork en de DCAT-AP plug-in voorzien. Hierdoor zijn telkens 3 sjablonen beschikbaar om gegevens (data en/of API’s) te beschrijven in Metadata Vlaanderen:
- Open community: Sjabloon voor ‘DCAT-AP VL 1.2’ werd geüpgraded naar ‘DCAT-AP VL 2.0’
  - Nu kunnen Open data volgens DCAT 2.0 beschreven worden, maar ook Open API’s vanaf nu beschreven worden
- Geo community: Het sjabloon blijft de GDI-Vlaanderen Best Practices voor metadata volgen. Deze data en API’s blijven dus in de ISO/INSPIRE-taal beschreven worden. Maar er is vanaf nu ook een download-output voorzien in RDF, die deze beschrijvingen in de (Geo)DCAT-taal voorstelt
  - Hiervoor werd de mapping-metadatastandaard ‘GeoDCAT-AP VL 2.0’ geïmplementeerd
- Niet-open én niet-geo (closed) community: Vanaf R3 is er ook een sjabloon beschikbaar volgens het basis-profiel ‘Metadata DCAT 2.0’
  - Vanaf nu kunnen ook de niet-open én niet-geo data en API’s worden beschreven

### Metadata-inhoud
- Alle native aangemaakte metadatarecords zijn ten gevolge van de upgrade naar DCAT2.0 zoveel als mogelijk gemigreerd
- Voor DCAT-feeds werd zoveel als mogelijk backward-compatibility behouden om de DCAT-AP VL 1.2 feeds nog steeds te kunnen oogsten

### Metadata-beheersysteem
- GeoNetwork 3.8:
  - Bugfixing en optimaliseren van kleine features
  - Alle aanpassingen, hierboven vermeld in het blokje over de metadata-standaard
- DCAT-AP plug-in:
  - De DCAT-AP plug-in 1.2 is uitgefaseerd en vervangen door de DCAT-AP plug-in 2.0
- Zoek-facets en indexing-mechanismen:
  - De zoek-facets en indexing-mechanismen werden aangepast zodat ze zowel op ISO/INSPIRE- als op DCAT-metadata-talen correct indexeren, zoeken en vinden


## [R2] - 31/05/2021

### Metadata-standaard
- Correctie van metadata wijzigingsdatum (dateStamp) van het type dateTime naar date; en dit voor dataset(serie)s en services
- Correctie voor de wijzigingsdatum (versionDate) van Objectencatalogi
    - Voor beide correcties volgen we nu de bepalingen in de standaard

### Metadata-inhoud
- Opschonen van metadata-inhoud ten gevolge van de INSPIRE Technical Guidelines 2.0; en vooral het verwijderen van INSPIRE-gerelateerde velden bij niet-INSPIRE dataset(serie)s en/of services

### Metadata-beheersysteem
- GeoNetwork 3.8: Bugfixing en optimaliseren van kleine features
  - Indexering verbeteren
  - Weergave verbeteren
  - Sjablonen verbeteren
  - Harvesting capabilities van diensten naar metadata verbeteren
  - Rechten corrigeren
  - Meerdere Objectencatalogi toevoegen kan nu ook
  - PDF-export is terug mogelijk
  - Hoofdlettergevoeligheid bij het oproepen van metadatarecords via hun identificatoren is opgelost


## [R1] - 16/11/2020

### De grootste verandering is dat metadata van Vlaamse Open data nu ook beschreven kunnen worden in het hoofdknooppunt, Metadata Vlaanderen
- Metadata van Vlaamse Open data => volgens de DCAT-AP VL standaard
  - Hiervoor is een 'DCAT-AP v1.2 plug-in voor GeoNetwork 3.8' gebouwd
  - Het harvesten van DCAT-feeds en het editeren van metadata van Vlaamse Open data gebeurt niet meer in het Vlaams Open Data Portaal, maar in Metadata Vlaanderen

### De andere veranderingen zijn grote moderniseringen
- Upgrade van de infrastructuur => de 'cloud'
- Upgrade van de technologie => metadata-beheersysteem 'GeoNetwork 3.8'
- Upgrade van de metadata-standaard voor het Geografische domein => conform de 'INSPIRE Technical Guidelines 2.0'



