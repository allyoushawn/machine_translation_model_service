.PHONY: install.sentiment.analysis.model.service.dependencies
install.sentiment.analysis.model.service.dependencies:
	echo "Installing dependencies for microservice" && \
	pip3 install -r ./sentiment_analysis_model_service/requirements.txt && \
	pip3 install -r ./base_microservice/requirements.txt && \
	pip3 install ./base_microservice ./sentiment_analysis_model_service

.PHONY: install.sentiment.analysis.model.service.test.dependencies
install.sentiment.analysis.model.service.test.dependencies:
	echo "Installing test dependencies" && \
	pip3 install -r ./monorepo_requirements.txt && \
	pip3 install -e ./sentiment_analysis_model_service/

.PHONY: run.sentiment.analysis.model.service.test
run.sentiment.analysis.model.service.test:
	echo "Running unit tests for microservice" &&\
	pytest -s ./sentiment_analysis_model_service/tests/unit --cov=sentiment_analysis_model_service/sentiment_analysis_model_service

.PHONY: run.sentiment.analysis.model.service.typing.test
run.sentiment.analysis.model.service.typing.test:
	echo "Running type checks for microservice" && \
	mypy ./sentiment_analysis_model_service/sentiment_analysis_model_service ./sentiment_analysis_model_service/tests/unit
