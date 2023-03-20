# Debugging Docker Networks

## Docker Networks

## list all networks

```bash
docker network ls
```

## inspect network

```bash
docker network inspect <network name>
```

## inspect networks from within a container

```bash
ip addr
```

## list all open ports within a container

```bash
netstat -tulpn
# or with ss
ss -lntu
# or
sudo ss -tulpn
```

 ## debugging a docker container with docker compose

to debug the docker container, open a bash in the container and run the following command:
    
    ```bash
    docker-compose exec --service-ports --rm labware-databank bash
    ```

    # --service-ports --rm labware-databank bash
    

