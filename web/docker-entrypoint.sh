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

    # Set Elasticsearch properties
    if [ "${GEONETWORK_ES_HOST}" != "localhost" ]; then
        sed -i "s#http://localhost:9200#${GEONETWORK_ES_PROTOCOL:="http"}://${GEONETWORK_ES_HOST}:${GEONETWORK_ES_PORT:="9200"}#g" "${JETTY_BASE}/webapps/${APP_NAME}/WEB-INF/web.xml" ;
        sed -i "s#es.host=localhost#es.host=${GEONETWORK_ES_HOST}#" "${JETTY_BASE}/webapps/${APP_NAME}/WEB-INF/config.properties" ;
    fi;

    if [ -n "${GEONETWORK_ES_PROTOCOL}" ] && [ "${GEONETWORK_ES_PROTOCOL}" != "http" ] ; then
        sed -i "s#es.protocol=http#es.protocol=${GEONETWORK_ES_PROTOCOL}#" "${JETTY_BASE}/webapps/${APP_NAME}/WEB-INF/config.properties" ;
    fi

    if [ -n "${GEONETWORK_ES_PORT}" ] && [ "$GEONETWORK_ES_PORT" != "9200" ] ; then
        sed -i "s#es.port=9200#es.port=${GEONETWORK_ES_PORT}#" "${JETTY_BASE}/webapps/${APP_NAME}/WEB-INF/config.properties" ;
    fi

    if [ -n "${GEONETWORK_ES_INDEX_RECORDS}" ] && [ "$GEONETWORK_ES_INDEX_RECORDS" != "gn-records" ] ; then
        sed -i "s#es.index.records=gn-records#es.index.records=${GEONETWORK_ES_INDEX_RECORDS}#" "${JETTY_BASE}/webapps/${APP_NAME}/WEB-INF/config.properties" ;
    fi

    if [ "${GEONETWORK_ES_USERNAME}" != "" ] ; then
        sed -i "s#es.username=#es.username=${GEONETWORK_ES_USERNAME}#" "${JETTY_BASE}/webapps/${APP_NAME}/WEB-INF/config.properties" ;
    fi

    if [ "${GEONETWORK_ES_PASSWORD}" != "" ] ; then
        sed -i "s#es.password=#es.password=${GEONETWORK_ES_PASSWORD}#" "${JETTY_BASE}/webapps/${APP_NAME}/WEB-INF/config.properties" ;
    fi

    if [ -n "${KB_URL}" ] && [ "$KB_URL" != "http://localhost:5601" ]; then
        sed -i "s#kb.url=http://localhost:5601#kb.url=${KB_URL}#" "${JETTY_BASE}/webapps/${APP_NAME}/WEB-INF/config.properties" ;
        sed -i "s#http://localhost:5601#${KB_URL}#g" "${JETTY_BASE}/webapps/${APP_NAME}/WEB-INF/web.xml" ;
    fi

    # Delegate on base image entrypoint to start jetty
    exec /docker-entrypoint.sh "$@"
else
    exec "$@"
fi
