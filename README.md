# ML Model Service
We treat each ml model service as a microservice, and we are using fastAPI for microservice deployment.
This repository could serve as multiple standalone services or be used as 
one of the backend ml service for ml service gateway ([repo](https://github.com/allyoushawn/mlservice)).

To run each ml model service, refer to the README in each service.

# Makefile
To run Makefile of each ml model service, using the following command:
```
make -f ./sentiment_analysis_model_service/Makefile install-microservice-dependencies
make -f ./sentiment_analysis_model_service/Makefile install-microservice-test-dependencies
make -f ./sentiment_analysis_model_service/Makefile run-microservice-unit-tests
make -f ./sentiment_analysis_model_service/Makefile run-microservice-typing-tests
```
