FROM python:alpine

USER root

RUN apk add --no-cache git

RUN apk add --no-cache zlib-dev bzip2-dev xz-dev

COPY ./start.sh /scripts/start.sh
WORKDIR /remsbwt
ENTRYPOINT ["/scripts/start.sh"]
