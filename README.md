# Microservice Example
Illustrate using fastAPI for microservice deployment.

```
cd /path/to/microservice_example
cd ..
docker build -t microservice:prod --target prod -f microservice_example/deployment/microservice/Dockerfile .
docker run --name microservice_local -it -p 4460:4460 microservice:prod
```

To stop and remove the container:
```
docker container stop microservice_local && docker container rm microservice_local
```
