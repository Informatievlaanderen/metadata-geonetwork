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