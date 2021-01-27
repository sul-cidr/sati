FROM postgres:12-alpine

LABEL author="Simon Wiles <simon.wiles@stanford.edu>"
EXPOSE 5432/tcp

COPY containers/sati-db/sati_db.init.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/sati_db.init.sh
