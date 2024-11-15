## Software required:
- **minikube**: create K8s cluster with single node
- **Docker**: Create custom image for WebApp
- **VM**: VirtualBox
- **kubectl**
- **VSCode**
---

## Cleating Kubernetes cluster using Minikube
- `minikube status`
- `minikube start --driver=virtualbox`
- `kubectl apply -f mongo-config.yaml`
- `kubectl apply -f mongo-secret.yaml`
- `kubectl apply -f mongo.yaml`
- `kubectl apply -f webapp.yaml`
---
**Get K8 info:**
- `kubectl get svc`
- `k get all`
- `minikube ip`
---
**Delete all**:
- `kubectl delete all --all`
- `kubectl delete all --all --all-namespaces`
- `minikube stop`
- `minikube delete`
---
## Building custom Docker image
- `docker build -t node-app:1.0 .` (.) refers to pick docker file from current dir

**Test run of image before pushing to *Docker Hub***
- `docker images`
- `docker run -d -port 3000:3000 node-app:1.0` run image on docer on port 3000
- `docker ps` see the status
---
**Push docker image to remote**
- `docker push <DOCKER_USERNAME>/<Image_Name>` 

## Run FastAPI script
- Make sure `.env` file has a valid OpenAI key with name `OPENAI_API_KEY`
- `pip install -r requirements.txt`
- `uvicorn main:app --reload --port 8000` : to run the server locally
- URL http://localhost:8000/query
- POST request body example, JSON
```
{
    "query": "How many pods are in the default namespace?"
}
```

- Expected response example:
```
{
    "query": "How many pods are in the default namespace?",
    "answer": "There are 5 pods in the default namespace."
}
```

![Result Image](result.png)
