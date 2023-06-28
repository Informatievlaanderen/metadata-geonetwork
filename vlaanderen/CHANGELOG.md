# Changelog
All notable changes to this project will be documented in this file. These changes are specific to Vlaanderen, important [core-geonetwork](https://github.com/geonetwork/core-geonetwork) changes are linked or embedded.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3-SNAPSHOT]
- TODO

## [1.0.2] - 2023-06-26
- Adding download link for RDF
- Adding VL/INSPIRE conformity keywords upon validation
- Enabled 'pin as favorite' functionality
- **core**
  - [High availability fix, allow configuration of separate html cache directory](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24976)
  - [High availability fix, define schema publication dir](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/25025)
  - [Work in progress: high availability](https://github.com/geonetwork/core-geonetwork/pull/6990)

## [1.0.1] - 2023-06-15
- Vlaanderen Geonetwork version now visible and automatically updating
- [Implement DCAT-ap metadata editor](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24798)
- **core** 
  - [merged core-geonetwork 4.2.5-SNAPSHOT changes](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24644)
    - Minor fixes and updates
    - Font-awesome library upgrade, minor icon changes
  - Fix issue in editor where reference to an element would be lost and recreated
  - Fix issue where `geonet` edit element where added multiple times
  - Fixed nullpointer bug in LocaleRedirects - [vlaanderen](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24802)

## [1.0.0] - 2023-06-09
- Introduced semver versioning
- [Add XML view/download options](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24005)
- [Added custom workflow](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/22731)
- [Added liquibase versioning for database versioning, disabling Geonetwork-managed updates](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/20246)
- [Cleanup of start-page "browse by" options](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/23629)
- [Customised facets](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/18729)
- Customised editor view
- [Introduce ACM/IDM as default authenticaiton layer](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/21672)
- [Introducing Cypress e2e testing](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/24170)
- Introduce DCAT editor - [pr1](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/22851), [pr2](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/23974)
- [Introducing DCAT plugin](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/18131) and [DCAT indexing](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/22605)
- Modified workflow with custom states
- [Porting 2005/2007 schemas and enforce default](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/18689)
- [Porting ISO editor](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/21740)
- [Porting thesauri of previous deployment](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/18736)
- **core**
  - Allow disabling the 'search map' - [core](https://github.com/geonetwork/core-geonetwork/pull/7071), [vlaanderen](https://agiv.visualstudio.com/Metadata/_workitems/edit/170315/)
  - [Allow disabling automatic database migration](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/21726)
  - [Config / add property file overlay](https://github.com/geonetwork/core-geonetwork/pull/6954), setting auto hibernate on startup
  - Copy resources to data dir - [core](https://github.com/geonetwork/core-geonetwork/pull/7110), [vlaanderen](https://agiv.visualstudio.com/Metadata/_git/MetadataGeonetwork/pullrequest/23983)
  - [Default tab configuration](https://github.com/geonetwork/core-geonetwork/pull/6986)
  - [Onhover mode for tooltips](https://github.com/geonetwork/core-geonetwork/pull/6987)
  - [Removal of magic numbers in workflow labels](https://github.com/geonetwork/core-geonetwork/pull/7104)
  - Upgraded to **core-geonetwork 4.2.5-SNAPSHOT**
    - Index performance improved, related to thesaurus and thumbnails
  - [Workflow / On Cancel / Properly remove draft from index](https://github.com/geonetwork/core-geonetwork/pull/7101)
  - [Workflow improvements](https://github.com/geonetwork/core-geonetwork/pull/7011)
