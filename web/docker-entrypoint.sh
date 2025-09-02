#!/bin/bash
set -e

export JAVA_OPTIONS=${JAVA_OPTS}

if ! command -v -- "$1" >/dev/null 2>&1 ; then
	set -- java -jar "$JETTY_HOME/start.jar" "$@"
fi

if [[ "$1" = jetty.sh ]] || [[ $(expr "$*" : 'java .*/start\.jar.*$') != 0 ]]; then
    # this is a command to run jetty

    # Sanity check: GEONETWORK_ES_HOST variable is mandatory
    if [ -z "${GEONETWORK_ES_HOST}" ]; then
        cat >&2 <<- EOWARN
			********************************************************************
			WARNING: Environment variable GEONETWORK_ES_HOST is mandatory

			GeoNetwork requires an Elasticsearch instance to store the index.
			Please define the variable GEONETWORK_ES_HOST with the Elasticsearch
			host name. For example

			docker run -e GEONETWORK_ES_HOST=elasticsearch geonetwork:${GN_VERSION}

			********************************************************************
		EOWARN
        exit 2
    fi;

    # Defines where you will deploy (subfolder). Default: 'geonetwork'.
    APP_NAME=root

    if [ -n "${KB_URL}" ] && [ "$KB_URL" != "http://localhost:5601" ]; then
        sed -i "s#kb.url=http://localhost:5601#kb.url=${KB_URL}#" "${JETTY_BASE}/webapps/${APP_NAME}/WEB-INF/config.properties" ;
        sed -i "s#http://localhost:5601#${KB_URL}#g" "${JETTY_BASE}/webapps/${APP_NAME}/WEB-INF/web.xml" ;
    fi

    # Delegate on base image entrypoint to start jetty
    exec /docker-entrypoint.sh "$@"
else
    exec "$@"
fi
