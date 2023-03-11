# Labop jupyter notebook entrypoint script

rdflib-endpoint serve --host 0.0.0.0 --port 8000 *.ttl
echo "RDFlib endpoint started"
echo "Starting SiLA server"