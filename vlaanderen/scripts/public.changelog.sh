#!/bin/bash
# variables
changesetFolder=../../liquibase/changesets
tempMdFileName=public.changelog.md
changelogFile=../CHANGELOG.md
publicChangeLogFileName=public.changelog.html

# test we have the prerequisite binaries available
if ! command -v sed &> /dev/null
then
    echo "sed could not be found"
    exit 1
fi

# prepare the changelog file, put it in the liquibase changesets folder so it can be picked up by liquibase
sed -E 's/\s*\-\s*\[pr.*//g' $changelogFile > $changesetFolder/$tempMdFileName
docker run --rm --volume "$(realpath $changesetFolder):/data" --user "$(id -u)":"$(id -g)" pandoc/minimal $tempMdFileName -o $publicChangeLogFileName
