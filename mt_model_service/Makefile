install-microservice-dependencies:
	echo "Installing dependencies for microservice" && \
	pip3 install -r ./mt_model_service/requirements.txt && \
	pip3 install -r ./base_microservice/requirements.txt && \
	pip3 install ./base_microservice ./mt_model_service

install-microservice-test-dependencies:
	echo "Installing test dependencies" && \
	pip3 install -r ./monorepo_requirements.txt && \
	pip3 install -e ./mt_model_service/

run-microservice-unit-tests:
	echo "Running unit tests for microservice" &&\
	pytest -s ./mt_model_service/tests/unit --cov=mt_model_service/mt_model_service

run-microservice-typing-tests:
	echo "Running type checks for microservice" && \
	mypy ./mt_model_service/mt_model_service ./mt_model_service/tests/unit