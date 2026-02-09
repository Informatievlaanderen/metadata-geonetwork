# Temporal database

For the postgresql a temporal copy is kept of the `public` schema. This is all done in-database, using trigger functions. The necessary setup is done through liquibase changesets, e.g., `00068-temporal-setup-function.sql`.

The code is based on an online example and tested against our setup. This seems to behave well for now.

## Impact

1. Each time GeoNetwork updates its database model, the respective change should be reflected in the temporal history.
2. Meta behaviour of the history tables should be monitored (size, update count, ...) in order to detect anomalies.

## Exclusions

Some default GeoNetwork database activity is causing unwanted temporal noise, resulting in massive data generation for no gain. Additionally, some tables do not have any useful impact on potential analyses. Below is a list of exclusions made in the temporal exercise, along with a justification for each.

- Table `settings`
  - GeoNetwork was updating the value for the mailServer each time it was accessed, causing spurious history.
  - This table contains a serialised json object so it potentially a source of flaky behaviour.
  - The table does not contain a lot of valuable information, in the context of analyses, so it was decided to remove it from history
