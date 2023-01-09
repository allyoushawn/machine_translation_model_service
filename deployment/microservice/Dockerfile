FROM python:3.9-slim AS base

ARG BUILD_ENV_ARG=local
ENV BUILD_ENV=$BUILD_ENV_ARG

RUN apt-get update -y && apt-get install -y gcc && apt-get install -y g++
COPY ./model_service/microservice/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY ./model_service/microservice /model_service/microservice
COPY ./model_service/base_microservice /model_service/base_microservice

RUN apt-get install make && \
    cd model_service && \
    make install-microservice-dependencies -f /model_service/microservice/Makefile

ARG gunicorn_port=4460
ENV gunicorn_port $gunicorn_port
EXPOSE $gunicorn_port
HEALTHCHECK CMD curl --fail http://localhost:4460/ || exit 0
RUN useradd -m -u  1000 nlp && \
    adduser nlp nogroup && \
    chmod o+x /model_service/microservice/service_start.sh

FROM base AS test
COPY ./model_service/monorepo_requirements.txt /model_service/monorepo_requirements.txt
COPY ./model_service/pytest.ini /model_service/pytest.ini
COPY ./model_service/mypy.ini /model_service/mypy.ini
WORKDIR model_service
RUN make install-microservice-test-dependencies -f /model_service/microservice/Makefile
CMD make run-microservice-unit-tests -f /model_service/microservice/Makefile && \
    make run-microservice-typing-tests -f /model_service/microservice/Makefile


FROM base AS prod
USER nlp
CMD sh /model_service/microservice/service_start.sh
