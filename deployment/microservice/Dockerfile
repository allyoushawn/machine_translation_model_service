FROM python:3.9-slim AS base

ARG BUILD_ENV_ARG=local
ARG SERVICE_NAME=machine_translation_model_service
ENV SERVICE_NAME $SERVICE_NAME
ENV BUILD_ENV=$BUILD_ENV_ARG

RUN apt-get update -y && apt-get install -y gcc && apt-get install -y g++
COPY ./$SERVICE_NAME/microservice/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY ./$SERVICE_NAME/microservice /$SERVICE_NAME/microservice
COPY ./$SERVICE_NAME/base_microservice /$SERVICE_NAME/base_microservice

RUN apt-get install make && \
    cd $SERVICE_NAME && \
    make install-microservice-dependencies -f /$SERVICE_NAME/microservice/Makefile

ARG gunicorn_port=4460
ENV gunicorn_port $gunicorn_port
EXPOSE $gunicorn_port
HEALTHCHECK CMD curl --fail http://localhost:4460/ || exit 0
RUN useradd -m -u  1000 nlp && \
    adduser nlp nogroup && \
    chmod o+x /$SERVICE_NAME/microservice/service_start.sh

FROM base AS test
COPY ./$SERVICE_NAME/monorepo_requirements.txt /$SERVICE_NAME/monorepo_requirements.txt
COPY ./$SERVICE_NAME/pytest.ini /$SERVICE_NAME/pytest.ini
COPY ./$SERVICE_NAME/mypy.ini /$SERVICE_NAME/mypy.ini
WORKDIR $SERVICE_NAME
RUN make install-microservice-test-dependencies -f /$SERVICE_NAME/microservice/Makefile
CMD make run-microservice-unit-tests -f /$SERVICE_NAME/microservice/Makefile && \
    make run-microservice-typing-tests -f /$SERVICE_NAME/microservice/Makefile


FROM base AS prod
USER nlp
CMD sh /$SERVICE_NAME/microservice/service_start.sh
