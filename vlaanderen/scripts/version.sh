#!/bin/bash
# get user input
usage="$(basename "$0") [-h] [-s]
--------------------------------------------------
Bump the version and create the necessary commits.
This can be run from a SNAPSHOT version. In that case, it will remove the SNAPSHOT and produce a 'finalisation' branch.
Afterwards, it bumps the version and produces a 'starting' branch for the new SNAPSHOT version.

where:
    -h  show this help text
    -s  start a snapshot
    -b  bump pom with specific type"

# where the pomfile lives
pomfile=../pom.xml
# current version, as set in the pom
current_version=$(mvn -f $pomfile help:evaluate -Dexpression=project.version -q -DforceStdout)
# where the changelog file lives
changelogfile=../CHANGELOG.md
# datestamp
today=$(date +%F)

function start_snapshot() {
  echo "starting snapshot"
  finalise_changelog "$current_version"
  bump_pom_snapshot
}

# pass X in 'X-SNAPSHOT' to be finalised
function finalise_changelog() {
  to_finalise=$1
  # replace the snapshot reference in changelog.md so we can't forget
  escaped_version=$(echo "$to_finalise" | sed -E 's/([][\.])/\\\1/g')
  echo "Escaped version: $escaped_version"
  echo "New version: $new_version"
  regex_from="s/## \[$escaped_version\].*/## [$new_version] - $today/"
  echo "Regex source: $regex_from"
  sed -E "$regex_from" -i $changelogfile
}

function bump_pom() {
  _bump_type=$1
  mvn -f $pomfile validate -D "bump-${_bump_type}" -q
}

function bump_pom_snapshot() {
  mvn -f $pomfile validate -D "add-snapshot" -q
}

while getopts ':hsb:' option; do
  case "$option" in
    h) echo "$usage"
       exit
       ;;
    s) start_snapshot
       ;;
    b) bump=$OPTARG
       bump_pom "$bump"
       ;;
    :) printf "missing argument for -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
   \?) printf "illegal option: -%s\n" "$OPTARG" >&2
       echo "$usage" >&2
       exit 1
       ;;
  esac
done
shift $((OPTIND - 1))

