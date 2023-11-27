# Orchestrators

## Kubernetes

```bash
kubectl apply -f orchestrators/k8s/mongodb-system.yaml && kubectl -n mongodb-system get pod -w
kubectl apply -f orchestrators/k8s/mongodb-init-job.yaml && kubectl -n mongodb-system get job -w

echo "MongoDB URI: mongodb://
$(kubectl -n mongodb-system get secret mongodb-root-user-credentials -o jsonpath='{.data.username}' | base64 --decode):
$(kubectl -n mongodb-system get secret mongodb-root-user-credentials -o jsonpath='{.data.password}' | base64 --decode)@
$(minikube -n mongodb-system service mongodb --url | sed 's/http:\/\///')" | tr -d '\n' && echo

kubectl apply -f orchestrators/k8s/redis-system.yaml && kubectl -n redis-system get pod -w

echo "redis-cli 
-h $(minikube -n redis-system service redis --url | cut -d'/' -f3 | cut -d':' -f1) 
-p $(minikube -n redis-system service redis --url | cut -d'/' -f3 | cut -d':' -f2)" | tr -d '\n' && echo

PING

FLUSHALL
FLUSHDB

INFO keyspace

CLIENT LIST
```