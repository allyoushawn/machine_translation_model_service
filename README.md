# Sentiment Analysis Model Service
Illustrate using fastAPI for microservice deployment. This repository could serve as a standalone service or be used as 
one of the backend ml service for ml service gateway ([repo](https://github.com/allyoushawn/mlservice)).


Following the following code to run the service:
```
cd /path/to/microservice_example
cd ..
docker build -t microservice:prod --target prod -f sentiment_analysis_model_service/deployment/microservice/Dockerfile .
docker run --name microservice_local -it -p 4460:4460 microservice:prod
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
docker container stop microservice_local && docker container rm microservice_local
```
