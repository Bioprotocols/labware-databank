# LabOP / SiLA Labware Databank and Ontology


This project provides a infrastructure for the development of an open ontology for scientific labware. 

It further develops a microservice that provides a SPARQL endpoint for querying the labware ontology and a SiLA 2.0 server that can be addressed, e.g. by lab-automation tasks.

Potential use cases for the ontology are:

 * Labware management : e.g. a labware can be stored in a labware management system
 * Labware identification : e.g. a labware can be identified by a barcode
 * Labware tracking : e.g. a labware can be tracked through the different steps of an experiment
 * Labware documentation: e.g. a labware can be documented with a picture, a description, a link to a protocol, etc.
 * Labware interoperability: does a certain labware fit into a certain instrument? does a certain lid fit onto a certain tube?
 * Labware automation: e.g. liquid handling robots
 * Labware recommendation: a LIMS system can recommend labware based on the desired experiment


This is a shared project between the [LabOP project](https://bioprotocols.org/) and the [SiLA 2.0](https://www.sila-standard.org/) working group project.

## Features

 * Labware Ontology
 * SPARQL endpoint for querying the labware ontology (including a web interface)
 * SiLA 2.0 compliant endpoint for querying the labware ontology

## Usage

### Installation

With docker-compose:

```bash
 wget https://raw.githubusercontent.com/Bioprotocols/labware-databank/main/docker/docker-compose.yml
 # or with curl:
 curl -O https://raw.githubusercontent.com/Bioprotocols/labware-databank/main/docker/docker-compose.yml

 # to build the docker containers, run in the directory where the docker-compose file is located:
 docker-compose build

 # to start the docker containers, run in the directory where the docker-compose file is located:
 docker-compose up
```

Now you can access the SPARQL endpoint web interface at [localhost:8008](http://localhost:8008/).
The jupyter-lab notebook is available at [localhost:8009](http://localhost:8009/).

The SiLA 2.0 server listens at [localhost:50052](http://localhost:50052/).

### Access using the SPARQL endpoint with curl

```bash
   curl -X POST -H "Content-Type: application/sparql-query" -H "Accept: application/sparql-results+json" --data "SELECT * WHERE { ?s ?p ?o } LIMIT 10" http://localhost:8008/sparql
```


### Access using the SiLA 2.0 server

We provided some examples of how to access the ontology using the SiLA 2.0 server. You can find them in the [examples](examples/) folder.
For the ease of playing with the SiLA 2.0 server, we also provide a jupyter-lab notebook with some examples. You can find it in the [jupyter](jupyter/) folder.

 

## Documentation

The Documentation can be found here: [openlab.gitlab.io/labop-labware-ontology](openlab.gitlab.io/labop-labware-ontology) or [labop-labware-ontology.gitlab.io](labop_labware_ontology.gitlab.io/)


## Credits

This package was created with Cookiecutter* and the `opensource/templates/cookiecutter-pypackage`* project template.

[Cookiecutter](https://github.com/audreyr/cookiecutter )
[opensource/templates/cookiecutter-pypackage](https://gitlab.com/opensourcelab/software-dev/cookiecutter-pypackage) 
