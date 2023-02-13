install-microservice-dependencies:
	echo "Installing dependencies for microservice" && \
	pip3 install -r ./sentiment_analysis_model_service/requirements.txt && \
	pip3 install -r ./base_microservice/requirements.txt && \
	pip3 install ./base_microservice ./sentiment_analysis_model_service

install-microservice-test-dependencies:
	echo "Installing test dependencies" && \
	pip3 install -r ./monorepo_requirements.txt && \
	pip3 install -e ./sentiment_analysis_model_service/

run-microservice-unit-tests:
	echo "Running unit tests for microservice" &&\
	pytest -s ./sentiment_analysis_model_service/tests/unit --cov=sentiment_analysis_model_service/sentiment_analysis_model_service

run-microservice-typing-tests:
	echo "Running type checks for microservice" && \
	mypy ./sentiment_analysis_model_service/sentiment_analysis_model_service ./sentiment_analysis_model_service/tests/unit