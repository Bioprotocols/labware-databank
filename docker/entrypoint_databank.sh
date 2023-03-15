# !/bin/bash
# Description: Entrypoint script for the databank container

# Labop jupyter notebook entrypoint script

echo "Starting databank uvicorn server"
# rdflib-endpoint serve --host 0.0.0.0 --port 8000 *.ttl &
cd /opt/labwaredb
echo "workdir:"
ls -Al
echo "Starting databank uvicorn server"
#uvicorn app.main:app --host 0.0.0.0 --port 8000 &
#rdflib-endpoint serve --host 0.0.0.0 --port 8000 *.ttl &

if [ "$SPARQL_SERVER" = "true" ]; then
    echo "Starting SPARQL server"
    #python3 /home/jovyan/sila_server.py
fi

# if [$SILA_SERVER == "true"]
if [ "$SILA_SERVER" = "true" ]; then
    echo "Starting SiLA server"
    #python3 /home/jovyan/sila_server.py
fi

echo "RDFlib endpoint started"
echo "Starting SiLA server .... --host 0.0.0.0  @port 50052"
python -m labop_labware_sila --insecure -d -v --port 50052
