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
    -b  bump pom with specific type
    -x  test"

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
  finalise_changelog
  bump_pom_snapshot
}

# pass X in 'X-SNAPSHOT' to be finalised
function finalise_changelog() {
  # replace "## [a.b.c-SNAPSHOT]" by "## [a.b.c] - xx/yy/zzzz"
  sed -E "s/## \[([0-9]+\.[0-9]+\.[0-9])-SNAPSHOT.*/## [\1] - $(date +%F)/g" -i $changelogfile
}

# add in the given version to the changelog, undated
function start_changelog_version() {
  _new_version=$1
  sed -E "s/(^The format is based on.*$)/\1\n\n\n## [${_new_version}]/" -i $changelogfile
}

function bump_pom() {
  _bump_type=$1
  mvn -f $pomfile validate -D "bump-${_bump_type}" -q
}

function bump_pom_snapshot() {
  mvn -f $pomfile validate -D "add-snapshot" -q
}

while getopts ':hsb:x' option; do
  case "$option" in
    h) echo "$usage"
       exit
      ;;
    s) start_snapshot
      ;;
    b) bump=$OPTARG
       bump_pom "$bump"
      ;;
    x) start_changelog_version "10.0.0-SNAPSHOT"
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

