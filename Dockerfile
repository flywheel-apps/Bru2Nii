FROM python:3.7.2-alpine3.9
MAINTAINER Flywheel <support@flywheel.io>
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}
RUN set -eux \
    && apk add --no-cache \
        bash \
        zip \
    && wget https://github.com/neurolabusc/Bru2Nii/releases/download/v1.0.20180303/Bru2_Linux.zip \
    && unzip -d /bin Bru2_Linux.zip \
    && rm Bru2_Linux.zip \
    && mkdir -p ${FLYWHEEL}/input ${FLYWHEEL}/output
COPY manifest.json manifest.json
COPY run run
ENTRYPOINT ["/flywheel/v0/run"]
