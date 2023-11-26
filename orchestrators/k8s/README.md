# Orchestrators

## Kubernetes

```
kubectl apply -f orchestrators/k8s/mongodb-system.yaml
kubectl apply -f orchestrators/k8s/mongodb-init-job.yaml
```

```
mongosh mongodb://root:X6d9r2SgJ8xQgpGL@<minikube service mongodb url>
```