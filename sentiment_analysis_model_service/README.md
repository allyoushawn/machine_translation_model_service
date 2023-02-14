# Sentiment Analysis Model Service
Illustrate using fastAPI for microservice deployment. This repository could serve as a standalone service or be used as 
one of the backend ml service for ml service gateway ([repo](https://github.com/allyoushawn/mlservice)).


Following the following code to run the service:
```
cd /path/to/ml_model_service
docker build -t sentiment_analysis_model_service:prod --target prod -f deployment/sentiment_analysis_model_service/Dockerfile .
docker run --name sentiment_analysis_model_service_local -it -p 4460:4460 sentiment_analysis_model_service:prod
```

An example cURL request to local server would be
```
curl -X POST http://127.0.0.1:4460/sentiment_analysis -H 'Content-Type: application/json' -d '{"text":"This is very good."}'
```

The response would be
```
{"request":{"text":"This is very good."},"response":{"word_num":4,"sentiment_score":3.0}}
```

To stop and remove the container:
```
docker container stop sentiment_analysis_model_service_local && docker container rm sentiment_analysis_model_service_local
```


# Microservice Template
Using sentiment analysis as an example. The service has two functions: sentiment analysis and word count.
