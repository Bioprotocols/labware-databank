# build with: docker build -t labware/hello-world .
# list with: docker images
# delete with: docker rmi labware/hello-world
# docker login: echo <token> |  docker login ghcr.io -u <username> --password-stdin
FROM alpine
CMD [ "echo", "Hello Labware World - github actions 1.1" ]