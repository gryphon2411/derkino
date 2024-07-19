#!/bin/bash

confirm() {
    echo
    read -p "Do you wish to create $1? (y/N) " yn
    case $yn in
        [Yy]* ) return 0;;
        * ) return 1;;
    esac
    echo
}

create_deploy_and_wait() {
    local yaml_file=$1

    kubectl apply -f $yaml_file

    local namespace=$(yq e 'select(.kind == "Namespace") | .metadata.name' $yaml_file)

    if [ -z "$namespace" ]; then
        namespace="default"
    fi

    local deployment_name=$(kubectl -n $namespace get deployments -o jsonpath='{.items[0].metadata.name}')

    echo -n -e "\nCreating deployment.apps/$deployment_name..."
    while [[ $(kubectl -n $namespace get deployments $deployment_name -o 'jsonpath={..status.conditions[?(@.type=="Available")].status}') != "True" ]]; do
        sleep 1
        echo -n "."
    done
    echo

    kubectl -n $namespace get deployments $deployment_name

    kubectl -n $namespace get pods -l app=$deployment_name
}

create_statefulset_and_wait() {
    local yaml_file=$1

    kubectl apply -f $yaml_file

    local namespace=$(yq e 'select(.kind == "Namespace") | .metadata.name' $yaml_file)
    if [ -z "$namespace" ]; then
        namespace="default"
    fi

    local statefulset_name=$(kubectl -n $namespace get statefulsets -o jsonpath='{.items[0].metadata.name}')

    echo -n -e "\nCreating statefulset.apps/$statefulset_name..."
    while true; do
        local replicas=$(kubectl -n $namespace get statefulsets $statefulset_name -o 'jsonpath={..status.replicas}')
        local readyReplicas=$(kubectl -n $namespace get statefulsets $statefulset_name -o 'jsonpath={..status.readyReplicas}')

        if [ "$replicas" == "$readyReplicas" ]; then
            break
        fi

        sleep 1
        echo -n "."
    done
    echo

    kubectl -n $namespace get statefulsets $statefulset_name

    kubectl -n $namespace get pods -l app=$statefulset_name
}

create_job_and_wait() {
    local yaml_file=$1

    kubectl apply -f $yaml_file

    local namespace=$(yq e 'select(.kind == "Job") | .metadata.namespace' $yaml_file)

    if [ -z "$namespace" ]; then
        namespace="default"
    fi

    local job_name=$(kubectl -n $namespace get jobs -o jsonpath='{.items[0].metadata.name}')

    echo -n -e "\nCreating job.batch/$job_name..."
    while [[ $(kubectl -n $namespace get jobs $job_name -o 'jsonpath={..status.conditions[?(@.type=="Complete")].status}') != "True" ]]; do
        sleep 1
        echo -n "."
    done
    echo

    kubectl -n $namespace get jobs $job_name

    kubectl -n $namespace get pods -l job-name=$job_name
}



helm_install_and_wait() {
    local namespace=$1
    local release_name=$2
    local chart=$3
    local version=$4
    local values_file=$5

    helm -n $namespace install $release_name $chart --version $version -f $values_file --create-namespace

    sleep 2

    echo -n -e "Installing $chart ($version)..."

    while [[ $(helm status $release_name -n $namespace --output json | jq -r '.info.status') != "deployed" ]]; do
        sleep 1
        echo -n "."
    done
    echo

    helm status $release_name -n $namespace
}

start_time=$(date +%s)

echo -e "\nProvisioning Derkino k8s cluster...\n"

minikube start --cpus=max --memory=max

if confirm "Mongodb system"; then
    create_statefulset_and_wait orchestrators/k8s/mongodb-system.yaml
    echo
    echo "MongoDB URI: mongodb://
$(kubectl -n mongodb-system get secret mongodb-root-user-credentials -o jsonpath='{.data.username}' | base64 --decode):
$(kubectl -n mongodb-system get secret mongodb-root-user-credentials -o jsonpath='{.data.password}' | base64 --decode)@
$(minikube -n mongodb-system service mongodb --url | sed 's/http:\/\///')" | tr -d '\n' && echo
fi

if confirm "Mongodb init"; then
    create_job_and_wait orchestrators/k8s/mongodb-init-job.yaml
    kubectl -n mongodb-system logs jobs/mongodb-init | jq -r '.message'
fi

if confirm "Postgres system"; then
    create_statefulset_and_wait orchestrators/k8s/postgres-system.yaml
    kubectl -n postgres-system get secret postgres-root-user-credentials -o jsonpath='{.data.username}' | base64 --decode
    kubectl -n postgres-system get secret postgres-root-user-credentials -o jsonpath='{.data.password}' | base64 --decode
    minikube -n postgres-system  service postgres --url
fi

if confirm "Redis-Stack system"; then
    create_statefulset_and_wait orchestrators/k8s/redis-stack-system.yaml
    echo
    echo "Redis URI: redis://
$(kubectl -n redis-stack-system get secret redis-stack-default-user-credentials -o jsonpath='{.data.username}' | base64 --decode):
$(kubectl -n redis-stack-system get secret redis-stack-default-user-credentials -o jsonpath='{.data.password}' | base64 --decode)@
$(minikube -n redis-stack-system service redis-stack --url | head -n 1 | sed 's/http:\/\///')" | tr -d '\n' && echo
fi

if confirm "Kafka system"; then
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm_install_and_wait kafka-system kafka bitnami/kafka 26.6.2 orchestrators/k8s/charts/kafka/values.yaml
    echo
    kubectl get secret kafka-user-passwords --namespace kafka-system -o jsonpath='{.data.client-passwords}' | base64 -d
fi

if confirm "Derkino auth service"; then
    create_deploy_and_wait orchestrators/k8s/auth-service-deployment.yaml
fi

if confirm "Derkino data service"; then
    create_deploy_and_wait orchestrators/k8s/data-service-deployment.yaml
fi

if confirm "Derkino trend service"; then
    create_deploy_and_wait orchestrators/k8s/trend-service-deployment.yaml
fi

if confirm "Derkino ui"; then
    create_deploy_and_wait orchestrators/k8s/ui-deployment.yaml
fi

if confirm "Prometheus system"; then
    helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
    helm_install_and_wait prometheus-system prometheus prometheus-community/prometheus 25.8.2 orchestrators/k8s/charts/prometheus/values.yaml
fi

if confirm "Grafana system"; then
    helm repo add grafana https://grafana.github.io/helm-charts
    helm_install_and_wait grafana-system grafana grafana/grafana 7.0.19 orchestrators/k8s/charts/grafana/values.yaml
    echo "admin"
    kubectl -n grafana-system get secret grafana -o jsonpath="{.data.admin-password}" | base64 --decode
    
    # Data sources:
    # - Type: Prometheus
    # - Name: prometheus-server
    # - Prometheus server URL: http://prometheus-server.prometheus-system
    # Query (permanent view): kafka_server_brokertopicmetrics_messagesinpersec_count{topic="title-searches"}
fi

end_time=$(date +%s)

time_duration=$((end_time - start_time))
minutes=$((time_duration / 60))
seconds=$((time_duration % 60))

echo -e "\nProvisioning Derkino k8s cluster done. took ${minutes}m ${seconds}s\n"