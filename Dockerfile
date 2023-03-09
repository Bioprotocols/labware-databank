# LARAsuite Dockerfile
# to build the docker image, call :
# docker build -f Dockerfile -t labops/labwaredb:0.0.1 .
# docker run -p 8089:8000 --name labwaredb labops/labwaredb:0.0.1 

# list with: docker images
# docker container ls -a
# delete with: 
# docker rm <container id>
# docker rmi labops/labwaredb:0.0.1
# docker login: echo <token> |  docker login ghcr.io -u <username> --password-stdin


# see also https://snyk.io/blog/best-practices-containerizing-python-docker/

# to get the digest (=sha fingerprint) run:
# docker images --digests | grep python

FROM python:3.10-slim-buster
# to minimize image size one could build like (https://mherman.org/presentations/dockercon-2018/#39):
# FROM python:3.6 as base
# COPY requirements.txt /
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt
# FROM python:3.6-alpine
# COPY --from=base /wheels /wheels
# COPY --from=base requirements.txt .
# RUN pip install --no-cache /wheels/* # flask, gunicorn, pycrypto
#COPY lara_django_config.env /etc/lara_django_config.env
# Keeps Python from generating .pyc files in the container
#ENV PYTHONDONTWRITEBYTECODE 1

ENV LANG=C.UTF-8\
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1\
    PROJECT_ROOT=/opt/labwaredb

ENV VIRTUAL_ENV=$PROJECT_ROOT/venv \
    DEBIAN_FRONTEND=noninteractive 

# Debian package caching
ARG APT_PROXY
RUN set -x \
    && if [ "${APT_PROXY}" ]; \
    then echo "Acquire::http { Proxy \"http://${APT_PROXY}\"; };" > /etc/apt/apt.conf.d/01proxy \
    ; fi

# build environment
#RUN apt-get update
#RUN apt-get install -y --no-install-recommends build-essential gcc 

RUN set -x \
    && adduser lara --disabled-password --disabled-login --no-create-home --gecos "" \
    # Create a virtualenv for the application dependencies.
    && python -V  # Print out python version for debugging

# Install dependencies.
COPY requirements "${PROJECT_ROOT}/requirements/"

#RUN set -a \
#    && . /etc/lara_django_config.env \
#    && set +a \
#    && echo venv: ${DEFAULT_DATABASE_NAME} 

# Set virtualenv environment variables. This is equivalent to running
# source /env/bin/activate. This ensures the application is executed within
# the context of the virtualenv and will have access to its dependencies.
# s. https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
RUN python3 -m venv $VIRTUAL_ENV 

# activating the virtual environment
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r $PROJECT_ROOT/requirements/base.txt

# Raspberry Pi installations
# psutil is needed by ARM builds otherwise gevent and gunicorn fail to start

# RUN UNAME=`uname -m` && if [ "${UNAME#*arm}" != $UNAME ]; then \
#     pip install --no-cache-dir \
#     psutil==$PYTHON_PSUTIL_VERSION \
# ; fi \


WORKDIR ${PROJECT_ROOT}
# copy main lara-django script
COPY --chown=lara:lara ontologies ${PROJECT_ROOT}/
#COPY  --chown=lara:lara --from=production-build ${VIRTUAL_ENV} ./venv

USER lara

RUN ls ${PROJECT_ROOT}

EXPOSE 8000
CMD ["rdflib-endpoint", "serve", "--host", "0.0.0.0", "--port", "8000",  "*.ttl"]

#CMD ["ls" , "-al"]


#ENTRYPOINT ["gunicorn", "--bind", ]
#CMD [ "0.0.0.0:8000", "lara_django.wsgi" ]
#ENTRYPOINT ["/opt/labdb/entrypoint.sh"]
#ENTRYPOINT exec "${PROJECT_ROOT}/entrypoint.sh"

# CMD python -m django --version
# CMD lara-django.py runserver 0.0.0.0:8080
