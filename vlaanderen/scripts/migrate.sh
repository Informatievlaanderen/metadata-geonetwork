#!/bin/bash

# before you go...
# 1. stop geonetwork and any program that accesses the database

# params
# dev/bet/prd
ENV=bet

# transfer data  one environment to another

# test case: bet to loc

outputfile=/tmp/dump.postgres

# the database where we copy FROM (won't be modified)
sourcehost=localhost
# same ports are used as in port-forward-db.sh
sourceport="unset"
if [[ $ENV == "prd" ]]
then
  sourceport=5435
elif [[ $ENV == "bet" ]]
then
  sourceport=5434
elif [[ $ENV == "dev" ]]
then
  sourceport=5433
else
  echo "Unknown env set, can't determine source database."
  exit 1
fi

sourceuser=geonetwork
sourcepassword=geonetwork
sourcedatabase=geonetwork
echo "source database: $sourceuser@$sourcehost:$sourceport/$sourcedatabase"

# the database we copy to (will be nuked)
targethost=localhost
targetport=5432

targetuser=geonetwork
targetpassword=geonetwork
targetdatabase=geonetwork
echo "target database: $targetuser@$targethost:$targetport/$targetdatabase"

read -p "Press enter to continue"

# prep
echo "removing file $outputfile"
rm $outputfile

# backup the source database
(
  export PGPASSWORD="$sourcepassword"
  pg_dump -Fc -f $outputfile -Z 9 -v -h "$sourcehost" -p "$sourceport" -U "$sourceuser" -d "$sourcedatabase"
)

# clear the target database
(
  export PGPASSWORD="$targetpassword"
  psql -U $targetuser -d postgres -p $targetport -h $targethost -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$targetdatabase'"
  psql -U $targetuser -d postgres -p $targetport -h $targethost -c "drop database if exists $targetdatabase"
)

# restore the dump
(
  export PGPASSWORD="$targetpassword"
  echo "Restoring dump $outputfile to $targethost:$targetport/$targetdatabase..."
  psql -U $targetuser -d postgres -p $targetport -h $targethost -c "create database $targetdatabase"
  pg_restore -U $targetuser -h $targethost -p $targetport -d $targetdatabase $outputfile
)
