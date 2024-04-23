FROM jetty:9.4.51-jdk11

# data dir for geonetwork, to be shared across instances
# subfolders are specified below, using the various env vars
ENV DATA_DIR /geonetwork-data
# run in '/' instead of '/geonetwork' (the default)
ENV WEBAPP_NAME root
ENV JAVA_OPTS -Dorg.eclipse.jetty.annotations.AnnotationParser.LEVEL=OFF \
        -Djava.security.egd=file:/dev/./urandom -Djava.awt.headless=true \
        -Xms512M -Xss512M -Xmx2G -XX:+UseConcMarkSweepGC \
        -Denv=prod \
        # don't use the geonetwork general data directory - default one is fine
        # -Dgeonetwork.dir=${DATA_DIR} \
        # don't override the following: they can be redeployed every time
        # -Dgeonetwork.codeList.dir=/var/lib/jetty/webapps/${WEBAPP_NAME}/WEB-INF/data/config/codelist \
        # -Dgeonetwork.schema.dir=/var/lib/jetty/webapps/${WEBAPP_NAME}/WEB-INF/data/config/schema_plugins
        # explicitly share these, these need to be present in the shared folder
        -Dgeonetwork.resources.dir=${DATA_DIR}/resources \
        -Dgeonetwork.upload.dir=${DATA_DIR}/upload \
        -Dgeonetwork.config.dir=${DATA_DIR}/config \
        -Dgeonetwork.data.dir=${DATA_DIR}/data \
        # separate this, otherwise it lands within the geonetwork.resources.dir folder
        -Dgeonetwork.htmlcache.dir=/var/lib/jetty/webapps/${WEBAPP_NAME}/WEB-INF/data/resources/htmlcache \
        -Dgeonetwork.schemapublication.dir=/var/lib/jetty/webapps/${WEBAPP_NAME}/WEB-INF/data/resources/schemapublication \
        -Dgeonetwork.indexConfig.dir=/var/lib/jetty/webapps/${WEBAPP_NAME}/WEB-INF/data/config/index \
        # improve performance of editing large forms
        -Djetty.httpConfig.requestHeaderSize=32768 \
        -Dorg.eclipse.jetty.server.Request.maxFormContentSize=500000 \
        -Dorg.eclipse.jetty.server.Request.maxFormKeys=8000

USER root
RUN apt-get -y update && \
    apt-get -y install --no-install-recommends unzip && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir -p /${DATA_DIR} && \
    chown -R jetty:jetty ${DATA_DIR} && \
    mkdir -p /var/lib/jetty/webapps/${WEBAPP_NAME} && \
    chown -R jetty:jetty /var/lib/jetty/webapps/${WEBAPP_NAME}

USER jetty
ENV GN_FILE geonetwork.war
COPY ./target/${GN_FILE} /var/lib/jetty/webapps/${WEBAPP_NAME}/${GN_FILE}

RUN cd /var/lib/jetty/webapps/${WEBAPP_NAME}/ && \
     unzip -q ${GN_FILE} && \
     rm ${GN_FILE}

# these files are added to the geonetwork context, see .dockerignore
COPY jetty-context-docker.xml /var/lib/jetty/webapps/${WEBAPP_NAME}.xml
COPY ./docker-entrypoint.sh /geonetwork-entrypoint.sh

# necessary on DevOps, +x flag is lost there
USER root
RUN chmod 755 /geonetwork-entrypoint.sh
USER jetty

ENTRYPOINT ["/geonetwork-entrypoint.sh"]

CMD ["java","-jar","/usr/local/jetty/start.jar"]

VOLUME [ "${DATA_DIR}" ]
