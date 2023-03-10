# Docker infrastructure


The simplest way to run the LabOP Labware Ontology is to use the docker containers. The docker containers are based on the [jupyter/scipy-notebook](https://hub.docker.com/r/jupyter/scipy-notebook/) docker image. The docker containers are available on [dockerhub](https://hub.docker.com/r/labopmuc/labop_labware_ontology/).

A docker-compose file is provided to start the docker containers. Follow the instructions below to start the docker containers with docker-compose.

## docker-compose

The docker-compose file is used to start the docker containers. It is located in the root directory of the repository.

to download the docker-compose file, run:

```bash
wget https://raw.githubusercontent.com/labopmuc/labop_labware_ontology/master/docker/docker-compose.yml
# or with curl
curl -O https://raw.githubusercontent.com/labopmuc/labop_labware_ontology/master/docker/docker-compose.yml
```

to build the docker containers, run in the directory where the docker-compose file is located:

```bash
docker-compose build
```

to start the docker containers, run:

```bash
docker-compose up
```



## docker

Every container can also be started individually.


## build docker container

to build the docker container, run:

```bash
docker build -t labop_labware_ontology .
```

## start docker container

to start the docker container, run:

```bash
ls
docker run -it # -p 8888:8888 -v $(pwd):/home/jovyan/work labop_labware_ontology
```

## debug docker container

to debug the docker container, run:

```bash
docker run -it --entrypoint /bin/bash labop_labware_ontology
```

## delete docker container

to delete the docker container, run:

```bash
docker container ls -a
# select the container id
docker rm <container id>
```

### delete docker image

to delete the docker image, run:

```bash
docker image ls
# select the image id
docker rmi <image id>
```

## start docker container with jupyter notebook

to start the docker container with jupyter notebook, run:

```bash

