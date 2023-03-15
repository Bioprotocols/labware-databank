# !/bin/bash
# Description: Entrypoint script for the databank container

# Labop jupyter notebook entrypoint script

rdflib-endpoint serve --host 0.0.0.0 --port 8000 *.ttl
# if [$SILA_SERVER == "true"]
if [ "$SILA_SERVER" = "true" ]; then
    echo "Starting SiLA server"
    #python3 /home/jovyan/sila_server.py
fi

echo "RDFlib endpoint started"
echo "Starting SiLA server .... --host 0.0.0.0  @port 50052"
labop_labware_sila --insecure --port 50052
