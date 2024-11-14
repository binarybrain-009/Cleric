- `minikube status`
- `minikube start --driver=virtualbox`
- `alias k=kubectl`
- `k get pods`
- `k apply -f mongo-config.yaml`
- `k apply -f mongo-secret.yaml`
- `k apply -f mongo.yaml`
- `k apply -f webapp.yaml`
- `k get all`
- `k get configmap`
- `k get secret`
- `k --help` **_OR_** `k --help <command>`
- `k describe <pod-name>`
- `k get svc`
- `minikube ip`

-

---

- `kubectl delete all --all`
- `kubectl delete all --all --all-namespaces`
- `minikube stop`
- `minikube delete`
- `pods`

---

- `docker build -t node-app:1.0 .` (.) refers to pick docker file from current dir
- `docker images`
- `docker run -d -port 3000:3000 node-app:1.0` run image on docer on port 3000
- `docker ps` see the status

---

- `pip install fastapi uvicorn python-dotenv`
- `uvicorn main:app --reload --port 8000`
- ``
