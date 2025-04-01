#!/bin/sh

# copy thesauri files from core to schema plugin folders
# only copy specific files, don't just bring over the whole folder

# copy files from here
SCRIPTS_FOLDER=$(dirname $0)
ROOT="$SCRIPTS_FOLDER/../.."

# general folders
SOURCE="$ROOT/web/src/main/webapp/WEB-INF/data/config/codelist/external/thesauri"
TARGET_ISO19139="$ROOT/schemas/iso19139/src/main/plugin/iso19139/thesauri"
TARGET_DCAT="$ROOT/schemas/dcat-ap/src/main/plugin/dcat-ap/thesauri"

# cleanup
rm -rfv "$TARGET_ISO19139"
mkdir -v -p "$TARGET_ISO19139/theme"
rm -rfv "$TARGET_DCAT"
mkdir -v -p "$TARGET_DCAT/place"
mkdir -v -p "$TARGET_DCAT/theme"

# copy specific theme files to dcat
cp -a "$SOURCE/theme/access-right-service.rdf" "$TARGET_DCAT/theme/access-right-service.rdf"
cp -a "$SOURCE/theme/access-right.rdf" "$TARGET_DCAT/theme/access-right.rdf"
cp -a "$SOURCE/theme/datatheme.rdf" "$TARGET_DCAT/theme/datatheme.rdf"
cp -a "$SOURCE/theme/file-type.rdf" "$TARGET_DCAT/theme/file-type.rdf"
cp -a "$SOURCE/theme/frequency.rdf" "$TARGET_DCAT/theme/frequency.rdf"
cp -a "$SOURCE/theme/language.rdf" "$TARGET_DCAT/theme/language.rdf"
cp -a "$SOURCE/theme/levensfase.rdf" "$TARGET_DCAT/theme/levensfase.rdf"
cp -a "$SOURCE/theme/licence-type.rdf" "$TARGET_DCAT/theme/licence-type.rdf"
cp -a "$SOURCE/theme/magda-domain.rdf" "$TARGET_DCAT/theme/magda-domain.rdf"
cp -a "$SOURCE/theme/media-types.rdf" "$TARGET_DCAT/theme/media-types.rdf"
cp -a "$SOURCE/theme/ontwikkelingstoestand.rdf" "$TARGET_DCAT/theme/ontwikkelingstoestand.rdf"
cp -a "$SOURCE/theme/protocol.rdf" "$TARGET_DCAT/theme/protocol.rdf"
cp -a "$SOURCE/theme/publisher-type.rdf" "$TARGET_DCAT/theme/publisher-type.rdf"
cp -a "$SOURCE/theme/resource-type.rdf" "$TARGET_DCAT/theme/resource-type.rdf"
cp -a "$SOURCE/theme/status.rdf" "$TARGET_DCAT/theme/status.rdf"
cp -a "$SOURCE/theme/TopicCategory.rdf" "$TARGET_DCAT/theme/TopicCategory.rdf"
# copy specific place files to dcat
cp -a "$SOURCE/place/GDI-Vlaanderenregions.rdf" "$TARGET_DCAT/place/GDI-Vlaanderenregions.rdf"
