# LabOP Labware Ontology

LabOP open ontology for scientific labware.


## Usage

### Installation

With docker-compose:

```bash
 curl https://raw.githubusercontent.com/Bioprotocols/labware-databank/main/docker/docker-compose.yml -o docker-compose.yml

 docker-compose up
```
Now you can access the SPARQL endpoint web interface at [localhost:8008](http://localhost:8008/).
The jupyter-lab notebook is available at [localhost:8888](http://localhost:8888/).

### Access using the SPARQL endpoint with curl

```bash
   curl -X POST -H "Content-Type: application/sparql-query" -H "Accept: application/sparql-results+json" --data "SELECT * WHERE { ?s ?p ?o } LIMIT 10" http://localhost:8008/sparql
```


### Access using the SiLA 2.0 server

We provided some examples of how to access the ontology using the SiLA 2.0 server. You can find them in the [examples](examples/) folder.
For the ease of playing with the SiLA 2.0 server, we also provide a jupyter-lab notebook with some examples. You can find it in the [jupyter](jupyter/) folder.

 
## Features

 * Labware Ontology
 * SPARQL endpoint for querying the labware ontology
 * SiLA 2.0 compliant endpoint for querying the labware ontology

## Documentation

The Documentation can be found here: [openlab.gitlab.io/labop-labware-ontology](openlab.gitlab.io/labop-labware-ontology) or [labop-labware-ontology.gitlab.io](labop_labware_ontology.gitlab.io/)


## Credits

This package was created with Cookiecutter* and the `opensource/templates/cookiecutter-pypackage`* project template.

[Cookiecutter](https://github.com/audreyr/cookiecutter )
[opensource/templates/cookiecutter-pypackage](https://gitlab.com/opensourcelab/software-dev/cookiecutter-pypackage) 
