# SHACL to Schematron conversion script

This script can be used to convert a JSON-LD [SHACL](https://www.w3.org/TR/shacl/) specification file to GeoNetwork valid schematron validation files.


# Delete schematron from db

When loading new schematrons **names**, the tables must be cleared first to then allow GeoNetwork to regenerate them
```sql
delete from schematroncriteria;
delete from schematroncriteriagroup;
delete from schematrondes;
delete from schematron;
```

## Install dependencies and run the script

Setup python environment:

```shell
sudo apt install python3.14-venv pip
```

Create virtual environment, install dependencies and run the script:
```shell
cd vlaanderen/scripts/shacl-to-schematron
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cd src
python main.py
```

## SHACL rules

See [configuration file](src/constants.py).


* dcat-ap 2.1.1 https://semiceu.github.io/DCAT-AP/releases/2.1.1/ / here as well: shapes, range, recommended, ...,
* dcat-ap 3.0.0 https://semiceu.github.io/DCAT-AP/releases/3.0.0/ / there are multiple files defined here (shapes.ttl, range.ttl, shapes_recommended.ttl),
* mobility 1.1.0 https://mobilitydcat-ap.github.io/mobilityDCAT-AP/releases/1.1.0/index.html
  * https://mobilitydcat-ap.github.io/mobilityDCAT-AP/releases/1.1.0/validationFiles/mobilitydcat-ap_shacl_shapes.ttl
* mobility 3.0.0 https://mobilitydcat-ap.github.io/mobilityDCAT-AP/drafts/latest/index.html / this one has two shacls, for basic and range constraints,
* healthdcat-ap 6 https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-6/ (based on dcat3, https://healthdataeu.pages.code.europa.eu/healthdcat-ap/releases/release-6/#validation-of-healthdcat-ap mentions multiple files, with an additional split for public and non-public
* https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat/ 
  * https://data.vlaanderen.be/doc/applicatieprofiel/metadata-dcat/erkendestandaard/2022-04-21/shacl/metadata-voor-services-ap-SHACL.ttl,
* https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL/erkendestandaard/2022-04-21/
  * https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL/erkendestandaard/2022-04-21/shacl/DCAT-AP-VL-20-SHACL.ttl
* https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL/ (current version, 3)
  * https://data.vlaanderen.be/doc/applicatieprofiel/DCAT-AP-VL/erkendestandaard/2026-02-12/shacl/DCAT-AP-VL-SHACL.ttl


Profile URI should match editor configuration. See https://github.com/metadata101/dcat-ap/blob/main/src/main/plugin/dcat-ap/dcat-profiles.xsl
