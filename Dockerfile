FROM python:3.7.3-alpine3.9
MAINTAINER Flywheel <support@flywheel.io>
ENV FLYWHEEL /flywheel/v0
WORKDIR ${FLYWHEEL}

RUN apk add --no-cache bash zip

ENV BRU2NII_VERSION v1.0.20180303
RUN set -eux \
    && wget https://github.com/neurolabusc/Bru2Nii/releases/download/${BRU2NII_VERSION}/Bru2_Linux.zip \
    && unzip -d /bin Bru2_Linux.zip \
    && rm Bru2_Linux.zip

ENV SDK_VERSION 6.1.0-dev.3
RUN pip install flywheel-sdk==${SDK_VERSION}

COPY manifest.json run.py ${FLYWHEEL}/
ENTRYPOINT ["bash"]
