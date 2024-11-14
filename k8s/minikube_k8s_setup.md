
# Minikube Setup and Kubernetes Operations on Ubuntu

## Introduction
This document outlines the steps and commands for setting up Minikube on Ubuntu and troubleshooting common issues related to Kubernetes node, pods, and SSH access.

## Minikube Setup

### Start Minikube
```bash
minikube start --driver=virtualbox
```

Output:
```
😄  minikube v1.34.0 on Ubuntu 24.04
✨  Using the virtualbox driver based on existing profile
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🔄  Restarting existing virtualbox VM for "minikube" ...
🐳  Preparing Kubernetes v1.31.0 on Docker 27.2.0 ...
    ▪ Generating certificates and keys ...
    ▪ Booting up control plane ...
    ▪ Configuring RBAC rules ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  Enabled addons: default-storageclass, storage-provisioner
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

### Check Minikube Status
```bash
minikube status
```
Output:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

### Retrieve Minikube IP
```bash
minikube ip
```
Output:
```
192.168.59.100
```

## SSH Access to Minikube Virtual Machine

### SSH into Minikube
```bash
ssh docker@192.168.59.100
```
You might encounter the following issue:
```
Permission denied, please try again.
docker@192.168.59.100: Permission denied (publickey,password,keyboard-interactive).
```

### Restart Minikube
```bash
minikube stop
minikube start
```

### Verify SSH Host Key Change
When attempting to SSH again, you might see a warning:
```
WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
```
To resolve this issue, remove the conflicting key:
```bash
ssh-keygen -f '/home/ub-karar/.ssh/known_hosts' -R '192.168.59.100'
```

### SSH with Correct Key
```bash
ssh -i $(minikube ssh-key) docker@192.168.59.100
```

Output:
```
$ docker ps
CONTAINER ID   IMAGE                        COMMAND                  CREATED          STATUS          PORTS     NAMES
351fcedeedf1   6e38f40d628d                 "/storage-provisioner"   10 minutes ago   Up 10 minutes             k8s_storage-provisioner_storage-provisioner_kube-system_47faef5a-9d6b-47de-8f64-07bb667d4dc6_3
...
```

### Exit SSH
```bash
exit
```

# Kubernetes Commands

### Check Kubernetes Cluster Info
```bash
kubectl cluster-info
```

Output:
```
Kubernetes control plane is running at https://192.168.59.100:8443
CoreDNS is running at https://192.168.59.100:8443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
```

### Get Node Status
```bash
kubectl get node
```

Output:
```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   25m   v1.31.0
```

### Get Kubernetes Namespaces
```bash
kubectl get namespaces
```

Output:
```
NAME              STATUS   AGE
default           Active   26m
kube-node-lease   Active   26m
kube-public       Active   26m
kube-system       Active   26m
```

### Get Pods in kube-system Namespace
```bash
kubectl get pods --namespace=kube-system
```

Output:
```
NAME                               READY   STATUS    RESTARTS      AGE
coredns-6f6b679f8f-877nt           1/1     Running   1 (17m ago)   28m
...
```

### Run an Nginx Pod
```bash
kubectl run nginx --image=nginx
```
Output:
```
pod/nginx created
```
