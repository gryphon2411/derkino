# Orchestrators

## Kubernetes

```bash
kubectl apply -f orchestrators/k8s/mongodb-system.yaml && kubectl -n mongodb-system get pod -w
kubectl apply -f orchestrators/k8s/mongodb-init-job.yaml && kkubectl -n mongodb-system get job -w
```

```bash
echo "URI: mongodb://
$(kubectl -n mongodb-system get secret mongodb-root-user-credentials -o jsonpath='{.data.username}' | base64 --decode):
$(kubectl -n mongodb-system get secret mongodb-root-user-credentials -o jsonpath='{.data.password}' | base64 --decode)@
$(minikube -n mongodb-system service mongodb --url | sed 's/http:\/\///')" | tr -d '\n' && echo
```