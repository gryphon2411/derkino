# Orchestrators

## Kubernetes

```bash
kubectl apply -f orchestrators/k8s/mongodb-system.yaml && kubectl -n mongodb-system get pod -w
kubectl apply -f orchestrators/k8s/mongodb-init-job.yaml && kubectl -n mongodb-system get job -w

echo "MongoDB URI: mongodb://
$(kubectl -n mongodb-system get secret mongodb-root-user-credentials -o jsonpath='{.data.username}' | base64 --decode):
$(kubectl -n mongodb-system get secret mongodb-root-user-credentials -o jsonpath='{.data.password}' | base64 --decode)@
$(minikube -n mongodb-system service mongodb --url | sed 's/http:\/\///')" | tr -d '\n' && echo

kubectl apply -f orchestrators/k8s/postgres-system.yaml && kubectl -n postgres-system get pod -w
kubectl -n postgres-system get secret postgres-root-user-credentials -o jsonpath='{.data.username}' | base64 --decode
kubectl -n postgres-system get secret postgres-root-user-credentials -o jsonpath='{.data.password}' | base64 --decode
minikube -n postgres-system  service postgres --url

kubectl apply -f orchestrators/k8s/redis-stack-system.yaml && kubectl -n redis-stack-system get pod -w
echo "default"
kubectl -n redis-stack-system get secret redis-stack-default-user-pass -o jsonpath='{.data.password}' | base64 --decode
minikube -n redis-stack-system service list

# https://artifacthub.io/packages/helm/bitnami/kafka
helm repo add bitnami https://charts.bitnami.com/bitnami

helm -n kafka-system install kafka bitnami/kafka --version 26.6.2 -f orchestrators/k8s/charts/kafka/values.yaml --create-namespace

kubectl get secret kafka-user-passwords --namespace kafka-system -o jsonpath='{.data.client-passwords}' | base64 -d

kubectl apply -f orchestrators/k8s/data-service-deployment.yaml
# Perform at least 1 search so all Kafka input topics will be created
kubectl apply -f orchestrators/k8s/trend-service-deployment.yaml

# https://artifacthub.io/packages/helm/prometheus-community/prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm -n prometheus-system install prometheus prometheus-community/prometheus --version 25.8.2 -f orchestrators/k8s/charts/prometheus/values.yaml --create-namespace
# Expression (temporary view): kafka_server_brokertopicmetrics_messagesinpersec_count{topic="title-searches"}

# https://artifacthub.io/packages/helm/grafana/grafana?modal=install
helm repo add grafana https://grafana.github.io/helm-charts

helm -n grafana-system install grafana grafana/grafana --version 7.0.19 -f orchestrators/k8s/charts/grafana/values.yaml --create-namespace

echo "admin"
kubectl -n grafana-system get secret grafana -o jsonpath="{.data.admin-password}" | base64 --decode
# Data sources:
# - Type: Prometheus
# - Name: prometheus-server
# - Prometheus server URL: http://prometheus-server.prometheus-system
# Query (permanent view): kafka_server_brokertopicmetrics_messagesinpersec_count{topic="title-searches"}
```

### Helm Cheatsheet 

```bash
helm list -A
```