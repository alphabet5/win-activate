#FROM python:3-alpine as stage1
#
#RUN find / -iname wheelhouse
#RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo
#RUN apk add --no-cache libressl-dev musl-dev curl bash perl
#RUN mkdir /out
#COPY ./build.sh ./build.sh
#RUN pip install virtualenv
#RUN ./build.sh

FROM python:3-slim-bullseye
LABEL maintainer="alphabet5"

RUN apt-get update && \
    apt-get -y install chromium-browser \
                       libnss3-dev && \

#RUN apk add --no-cache bash
#COPY --from=stage1 /cffi-*.whl /whl/
#COPY --from=stage1 /cryptography-*.whl /whl/
#COPY --from=stage1 /pycparser-*.whl /whl/
#COPY --from=stage1 /openssl-*.whl /whl/

COPY dist/win_activate-*-py2.py3-none-any.whl /whl/
RUN pip install --no-cache-dir /whl/*
#RUN pip install --no-cache-dir pypsrp yamlarg keyring selenium
#RUN rm -rf /whl

# COPY cert_checker.py ./

#CMD [ "python", "./cert_checker.py" ]
COPY docker-helpers/entrypoint.sh /sbin/entrypoint.sh
RUN chmod 755 /sbin/entrypoint.sh
ENTRYPOINT ["/sbin/entrypoint.sh"]