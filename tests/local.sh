#!/bin/bash

echo "Create kind cluster"
kind create cluster

echo "Build and deploy to kind the operator"
docker build -t ghcr.io/k8spin/grafana-multi-tenant-operator:e2e .
kind load docker-image ghcr.io/k8spin/grafana-multi-tenant-operator:e2e

echo "Deploy Grafana Server"
helm repo add grafana https://grafana.github.io/helm-charts --force-update
helm repo update
helm upgrade --install grafana --set adminPassword=admin grafana/grafana
kubectl wait --for=condition=available --timeout=600s deployment/grafana

echo "Deploy Grafana Multi-Tenant Operator"
kubectl create secret generic grafana-multi-tenant-operator --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_HOST=grafana.default.svc.cluster.local --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_USERNAME=admin --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_PASSWORD=admin
helm upgrade --install k8spin --set image.tag=e2e deploy/charts/grafana-multi-tenant-operator
kubectl wait --for=condition=available --timeout=600s deployment/k8spin-grafana-multi-tenant-operator

echo "Deploy examples"
kubectl apply -f examples/

echo "Deploy e2e tests"
kubectl apply -f tests/e2e.yaml
kubectl wait --for=condition=complete --timeout=120s job/e2e

echo "Delete local Cluster"
kind delete cluster
