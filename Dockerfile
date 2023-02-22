# build with: docker build -t labware/hello-world .
# list with: docker images
FROM alpine
CMD [ "echo", "Hello Labware World - github actions" ]