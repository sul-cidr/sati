FROM python:3.8-alpine

LABEL author="Simon Wiles <simon.wiles@stanford.edu>"
ENV PYTHONUNBUFFERED=1

# Note: COPY statements are relative to the build context, which
#       is set to the repo root in docker-compose.yml.

WORKDIR /opt/sati
COPY src /opt/sati
COPY containers/sati-app/entrypoint.sh /docker-entrypoint.sh

RUN apk --no-cache add --virtual build-deps gcc python3-dev musl-dev libjpeg \
  && apk --no-cache add tini postgresql-dev jpeg-dev zlib-dev \
  && pip install pipenv gunicorn \
  && pipenv install --deploy --system --ignore-pipfile \
  && apk del build-deps \
  && chmod 755 "/docker-entrypoint.sh"

ENTRYPOINT ["/sbin/tini", "--", "/docker-entrypoint.sh"]
