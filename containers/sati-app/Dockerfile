FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1

# Note: COPY statements are relative to the build context, which
#       is set to the repo root.


WORKDIR /opt/sati

COPY src /opt/sati

RUN apk --no-cache add --virtual build-deps gcc python3-dev musl-dev libjpeg
RUN apk --no-cache add tini postgresql-dev jpeg-dev zlib-dev
RUN pip install pipenv
RUN pipenv install $(test "$DJANGO_ENV" == production || echo "--dev") --deploy --system --ignore-pipfile
RUN apk del build-deps

COPY containers/sati-app/entrypoint.sh /docker-entrypoint.sh
RUN chmod 755 "/docker-entrypoint.sh"
ENTRYPOINT ["/sbin/tini", "--", "/docker-entrypoint.sh"]
