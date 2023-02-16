# Machine Translation Model Service
Illustrate using fastAPI for microservice deployment. This repository could serve as a standalone service or be used as 
one of the backend ml service for ml service gateway ([repo](https://github.com/allyoushawn/mlservice)).


Following the following code to run the service:
```
cd /path/to/ml_model_service
docker build -t mt_model_service:prod --target prod -f deployment/mt_model_service/Dockerfile .
docker run --name mt_model_service_local -it -p 4461:4461 mt_model_service:prod
```

An example cURL request to local server would be
```
curl -X POST http://127.0.0.1:4461/machine_translation -H 'Content-Type: application/json' -d '{"text":"This is very good."}'
```

The response would be
```
{{"request":{"text":"This is very good."},"response":{"word_num":4,"translated_text":"这是 非常 好 的 。"}}
```

To stop and remove the container:
```
docker container stop mt_model_service_local && docker container rm mt_model_service_local
```

## Run the service with GPU
1. Make sure the `MODEL_PATH` in paths.py is pointing to a GPU-trained model. You might need to make sure MANIFEST.in also specify the GPU-based model.
2. Change the corresponding docker cmds to the following and the service would use GPU.
```
docker build -t mt_model_service_gpu:prod --target prod -f deployment/mt_model_service/Dockerfile.gpu .
docker run --name mt_model_service_gpu_local --gpus all -it -p 4461:4461 mt_model_service_gpu:prod
docker container stop mt_model_service_gpu_local && docker container rm mt_model_service_gpu_local
```

# Note
- Copying model files, which are relatively large, into docker image is not a good practice. We should try to use other techniques like docker mounting to improve the service.

# Microservice Template
Using sentiment analysis as an example. The service has two functions: sentiment analysis and word count.
