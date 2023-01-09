FROM python:3.9-slim AS base

ARG BUILD_ENV_ARG=local
ENV BUILD_ENV=$BUILD_ENV_ARG

RUN apt-get update -y && apt-get install -y gcc && apt-get install -y g++
COPY ./microservice_example/microservice/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY ./microservice_example/microservice /microservice_example/microservice
COPY ./microservice_example/base_microservice /microservice_example/base_microservice

RUN apt-get install make && \
    cd microservice_example && \
    make install-microservice-dependencies -f /microservice_example/microservice/Makefile

ARG gunicorn_port=4460
ENV gunicorn_port $gunicorn_port
EXPOSE $gunicorn_port
HEALTHCHECK CMD curl --fail http://localhost:4460/ || exit 0
RUN useradd -m -u  1000 nlp && \
    adduser nlp nogroup && \
    chmod o+x /microservice_example/microservice/service_start.sh

FROM base AS test
COPY ./microservice_example/monorepo_requirements.txt /microservice_example/monorepo_requirements.txt
COPY ./microservice_example/pytest.ini /microservice_example/pytest.ini
COPY ./microservice_example/mypy.ini /microservice_example/mypy.ini
WORKDIR microservice_example
RUN make install-microservice-test-dependencies -f /microservice_example/microservice/Makefile
CMD make run-microservice-unit-tests -f /microservice_example/microservice/Makefile && \
    make run-microservice-typing-tests -f /microservice_example/microservice/Makefile


FROM base AS prod
USER nlp
CMD sh /microservice_example/microservice/service_start.sh
