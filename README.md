# hyphen-platform-challenge
Platform Engineering Challenge for Hyphen Group

This repo contains code that
1) Terraform infra stack to deploy k8s (kind) cluster, promethus-stack, ingress-controller
2) service stack that deploy foo and bar service using skaffold
3) metric exporter to export the input promql data in csv format

## Prerequisites
1. Have `Docker` and the `Kubernetes CLI` (`kubectl`) installed together with `Minikube` (https://kubernetes.io/docs/tasks/tools/)
2. skaffold CLI (`skaffold`) for managing helm deployment

## Getting started
1. Clone the repository
2. Configure `Docker` to use the `Docker daemon` in your kubernetes cluster via your terminal: `eval $(minikube docker-env)`

## Infra Deployment
1. K8s Kind Cluster
```shell
cd infra/k8s
terraform plan && terraform apply
```
2. kube-promethus-stack
```shell
cd infra/promethus
terraform plan && terraform apply

To Import Dashboard for k8s and nginx-controller
```shell
export POD_NAME=$(kubectl get pods --namespace monitoring -l "app=grafana" -o jsonpath="{.items[0].metadata.name}")
kubectl --namespace monitoring port-forward $POD_NAME 3000
```
* Open http://localhost:3000/dashboard/import
* Grafana dashboard username and password can be retrieved from secret(`prometheus-grafana`).
* Upload JSON from promethus/dashboards, configure Prometheus as Data source
```

3. Nginx Ingress controller
```shell
cd infra/nginx-ingress
terraform plan && terraform apply
```

## Service Deployment
1. Deploy `Foo API` in service/foo/deploy folder: `skaffold deploy -t <version:latest>`
2. Deploy `Bar API` in service/bar/deploy folder: `skaffold deploy -t <version:latest>`
You can check the status of the pods, services and deployments.

## Start making requests
Now you can use the `API`
1. foo API: `curl -H "Content-Type: application/json" localhost/foo`
2. bar API: `curl -H "Content-Type: application/json" localhost/bar`


## Metrics Exporter
1. we can generate some sample load by making some requests using CURL
```shell
while true; do
 curl -X GET localhost/foo
done
```
2. Expose the Prometheus API via localhost/Ingress
```shell
export POD_NAME=$(kubectl get pods --namespace monitoring -l "app=prometheus,component=server" -o jsonpath="{.items[0].metadata.name}")
kubectl --namespace monitoring port-forward $POD_NAME 9090
```
3. Specify the Promql in the promql file and execute python prom_csv.py
