# local installation

## Requirements

## Installation

    # ontology development
    pip install labop-labware-ontology@git+https://github.com/bioprotocols/labware-databank@develop

    # sila server
    pip install "git+https://github.com/bioprotocols/labware-databank.git#egg=labop_labware_sila&subdirectory=SiLA"
    
    # running the sila server locally
    python -m labop_labware_sila --insecure
