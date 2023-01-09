FROM python:3.9-slim AS base

ARG BUILD_ENV_ARG=local
ENV BUILD_ENV=$BUILD_ENV_ARG

RUN apt-get update -y && apt-get install -y gcc && apt-get install -y g++
COPY ./machine_translation_model_service/microservice/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY ./machine_translation_model_service/microservice /machine_translation_model_service/microservice
COPY ./machine_translation_model_service/base_microservice /machine_translation_model_service/base_microservice

RUN apt-get install make && \
    cd machine_translation_model_service && \
    make install-microservice-dependencies -f /machine_translation_model_service/microservice/Makefile

ARG gunicorn_port=4460
ENV gunicorn_port $gunicorn_port
EXPOSE $gunicorn_port
HEALTHCHECK CMD curl --fail http://localhost:4460/ || exit 0
RUN useradd -m -u  1000 nlp && \
    adduser nlp nogroup && \
    chmod o+x /machine_translation_model_service/microservice/service_start.sh

FROM base AS test
COPY ./machine_translation_model_service/monorepo_requirements.txt /machine_translation_model_service/monorepo_requirements.txt
COPY ./machine_translation_model_service/pytest.ini /machine_translation_model_service/pytest.ini
COPY ./machine_translation_model_service/mypy.ini /machine_translation_model_service/mypy.ini
WORKDIR machine_translation_model_service
RUN make install-microservice-test-dependencies -f /machine_translation_model_service/microservice/Makefile
CMD make run-microservice-unit-tests -f /machine_translation_model_service/microservice/Makefile && \
    make run-microservice-typing-tests -f /machine_translation_model_service/microservice/Makefile


FROM base AS prod
USER nlp
CMD sh /machine_translation_model_service/microservice/service_start.sh
