#!/bin/bash

echo "BUILD_ENV is $BUILD_ENV"
if [ "$BUILD_ENV" == "jenkins" ]; then
    echo "Downloading credentials"
else
    echo "BUILD_ENV not jenkins, no need to download credientials"
fi

# start fastapi service

gunicorn_port=4460

if [ "$BUILD_ENV" == "jenkins" ]; then
    echo "Start service with credentials"
    gunicorn -w 3 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$gunicorn_port microservice.entrypoint --certfile=/path/to/file.crt --keyfile=/path/to/file.key
else
    echo "Start service without credentials"
    gunicorn -w 3 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$gunicorn_port microservice.entrypoint
fi
