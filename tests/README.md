# E2E Tests

Follow this guide to run e2e tests locally:

## Manual

First, create a local kind cluster:

```bash
$ kind create cluster
```

Then build and deploy the operator:

```bash
$ docker build -t ghcr.io/k8spin/grafana-multi-tenant-operator:e2e .
$ kind load docker-image ghcr.io/k8spin/grafana-multi-tenant-operator:e2e
$ helm repo add grafana https://grafana.github.io/helm-charts --force-update
$ helm repo update
$ helm upgrade --install grafana --set adminPassword=admin grafana/grafana
$ kubectl wait --for=condition=available --timeout=600s deployment/grafana
$ kubectl create secret generic grafana-multi-tenant-operator --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_HOST=grafana.default.svc.cluster.local --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_USERNAME=admin --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_PASSWORD=admin
$ helm upgrade --install k8spin --set image.tag=e2e deploy/charts/grafana-multi-tenant-operator
$ kubectl wait --for=condition=available --timeout=600s deployment/k8spin-grafana-multi-tenant-operator
```

Deploy a few examples then run e2e tests:

```bash
$ kubectl apply -f examples/
$ kubectl apply -f tests/e2e.yaml
$ kubectl wait --for=condition=complete --timeout=600s job/e2e
```

Teardown the local cluster:

```bash
$ kind delete cluster
```

## Script

All these commands are available in a single bash script.

```bash
$ ./tests/local.sh
```
