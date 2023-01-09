install-microservice-dependencies:
	echo "Installing dependencies for microservice" && \
	pip3 install -r ./microservice/requirements.txt && \
	pip3 install -r ./base_microservice/requirements.txt && \
	pip3 install ./base_microservice ./microservice

install-microservice-test-dependencies:
	echo "Installing test dependencies" && \
	pip3 install -r ./monorepo_requirements.txt && \
	pip3 install -e ./microservice/

run-microservice-unit-tests:
	echo "Running unit tests for microservice" &&\
	pytest -s ./microservice/tests/unit --cov=microservice/microservice

run-microservice-typing-tests:
	echo "Running type checks for microservice" && \
	mypy ./microservice/microservice ./microservice/tests/unit