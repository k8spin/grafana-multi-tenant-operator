# Quick Start

The quick start guide walks through the process of setting up RBAC, operator deployment
and creating a Grafana Organization with an associated User.

## Prerequisites

- [Grafana instance](https://github.com/grafana/grafana).
    - Admin user *(basic auth)* credentials.
- Access to a [Kubernetes Cluster](https://github.com/kubernetes/kubernetes)
    - [kubectl](https://github.com/kubernetes/kubectl)

# Deployment Options

* [Using Helm](#deployment-with-helm)
* [Using Manifests](#deployment-with-manifests)

# Deployment with Helm

> NOTE: You will need the Helm binary installed on your local environment to use this deployment method.

You can use the Helm command-line tool to deploy the operator into your cluster. The CustomResourceDefinitions will be automatically
deployed with the Helm chart.

Before deploying the Grafana multi-tenant operator, create a secret with the following variables:

- `GRAFANA_MULTI_TENANT_OPERATOR_HOST`: [REQUIRED] Grafana endpoint. *Example: `grafana.monitoring.svc.cluster.local:3000`*
- `GRAFANA_MULTI_TENANT_OPERATOR_PORT`: [OPTIONAL] Grafana service port. *Defaults to `None`.*
- `GRAFANA_MULTI_TENANT_OPERATOR_PROTOCOL`: [OPTIONAL] Scheme to use. *Defaults to `http`.*
- `GRAFANA_MULTI_TENANT_OPERATOR_VERIFY`: [OPTIONAL] SSL Verification check. *Defaults to `True`.*
- `GRAFANA_MULTI_TENANT_OPERATOR_TIMEOUT`: [OPTIONAL] Timeout value. *Defaults to `5.0`.*
- `GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_USERNAME`: [OPTIONAL] Admin user. Default value: `admin`.
- `GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_PASSWORD`: [REQUIRED] Admin user password.

```bash
$ kubectl create secret generic grafana-multi-tenant-operator \
    --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_HOST=my_grafana_host \
    --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_USERNAME=admin \
    --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_PASSWORD=my_admin_password
```

Deploy the Helm chart:

```bash
$ helm repo add grafana-multi-tenant-operator https://k8spin.github.io/grafana-multi-tenant-operator/charts --force-update
"grafana-multi-tenant-operator" has been added to your repositories
$ helm upgrade --install k8spin grafana-multi-tenant-operator/grafana-multi-tenant-operator
```

or by:

```bash
$ helm install grafana-multi-tenant-operator deploy/charts/grafana-multi-tenant-operator
```

## Deployment with Manifests

Setup RBAC for the Grafana multi-tenant operator and its related resources:

```bash
$ kubectl create -f deploy/service_account.yaml
serviceaccount/grafana-multi-tenant-operator created
$ kubectl create -f deploy/role.yaml
role.rbac.authorization.k8s.io/grafana-multi-tenant-operator created
$ kubectl create -f deploy/role_binding.yaml
rolebinding.rbac.authorization.k8s.io/grafana-multi-tenant-operator created
```

Deploy the Grafana multi-tenant CRDs:

```bash
$ kubectl create -f deploy/crds.yaml
customresourcedefinition.apiextensions.k8s.io/organizations.grafana.k8spin.cloud created
customresourcedefinition.apiextensions.k8s.io/users.grafana.k8spin.cloud created
customresourcedefinition.apiextensions.k8s.io/dashboards.grafana.k8spin.cloud created
customresourcedefinition.apiextensions.k8s.io/datasources.grafana.k8spin.cloud created
```

Before deploying the Grafana multi-tenant operator, create a secret with the following variables:

- `GRAFANA_MULTI_TENANT_OPERATOR_HOST`: [REQUIRED] Grafana endpoint. *Example: `grafana.monitoring.svc.cluster.local:3000`*
- `GRAFANA_MULTI_TENANT_OPERATOR_PORT`: [OPTIONAL] Grafana service port. *Defaults to `None`.*
- `GRAFANA_MULTI_TENANT_OPERATOR_PROTOCOL`: [OPTIONAL] Scheme to use. *Defaults to `http`.*
- `GRAFANA_MULTI_TENANT_OPERATOR_VERIFY`: [OPTIONAL] SSL Verification check. *Defaults to `True`.*
- `GRAFANA_MULTI_TENANT_OPERATOR_TIMEOUT`: [OPTIONAL] Timeout value. *Defaults to `5.0`.*
- `GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_USERNAME`: [OPTIONAL] Admin user. Default value: `admin`.
- `GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_PASSWORD`: [REQUIRED] Admin user password.

```bash
$ kubectl create secret generic grafana-multi-tenant-operator \
    --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_HOST=my_grafana_host \
    --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_USERNAME=admin \
    --from-literal=GRAFANA_MULTI_TENANT_OPERATOR_ADMIN_PASSWORD=my_admin_password
```

Deploy the Grafana multi-tenant operator:

```bash
$ kubectl create -f deploy/operator.yaml
```

Verify that Grafana multi-tenant operator is up and running:

```bash
$ kubectl get deployment
NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
grafana-multi-tenant-operator   1/1     1            1           13h
```


## Create an example Organization

Create an Organization

```bash
$ kubectl apply -f examples/example.com-grafana-org.yaml
organization.grafana.k8spin.cloud/example.com created
```

Verify the Organization CR contains an Grafana Organization identifier:

```bash
$ kubectl describe org example.com
$ echo "Parsing with jq"
"Parsing with jq"
$ kubectl get org example.com -o json | jq -r .status.create_organization.orgId
3
```

You can also see it at `my_grafana_host` site:

![example.com Organization @ Grafana](../assets/example.com.png)


> **IMPORTANT: Using the Organization object to manage datasources is DEPRECATED. Use the Datasource CRD instead.**

Edit the Organization cr adding a datasource:

```bash
$ kubectl edit org example.com
organization.grafana.k8spin.cloud/example.com edited
$ kubectl get org example.com -o yaml
apiVersion: grafana.k8spin.cloud/v1
kind: Organization
metadata:
  finalizers:
  - kopf.zalando.org/KopfFinalizerMarker
  name: example.com
  namespace: default
spec:
  datasources:
  - data: |
      {
        "name": "Prometheus",
        "type": "prometheus",
        "access": "proxy",
        "url": "http://prometheus-operated.default.svc.cluster.local:9090",
        "basicAuth": false
      }
    name: Prometheus
```
Also if you are using another datasource like 'Cloudwatch'

```bash
$ kubectl edit org example.com
organization.grafana.k8spin.cloud/example.com edited
$ kubectl get org example.com -o yaml
apiVersion: grafana.k8spin.cloud/v1
kind: Organization
metadata:
  finalizers:
  - kopf.zalando.org/KopfFinalizerMarker
  name: example.com
  namespace: default
spec:
  datasources:
  - data: |
      {
        "name": "Cloudwatch",
        "type": "cloudwatch",
        "url": "http://monitoring.{{region}}.amazonaws.com",
        "access": "proxy",
        "jsonData": {
          "authType": "default",
          "assumeRoleArn": "arn:aws:iam::{{account}}:role/grafana-iam-role",
          "defaultRegion": "{{region}}"
        }
      }
    name: Cloudwatch
```
> Replace {{region}} according your configuration. You can find here [Amazon CloudWatch URL](https://docs.aws.amazon.com/general/latest/gr/cw_region.html) all endpoints. If you are using another "authType" for Cloudwatch or a different datasources you have more JSON examples here [Grafana Data source API](https://grafana.com/docs/grafana/latest/http_api/data_source/)


Switch to the example.com organization and navigate to datasources:

![Switch to example.com organization](../assets/switch-organization.png)

![Datasources at example.com organization](../assets/example.com.datasources.png)


## Create an Organization Datasource with a CustomResource

You can create organization Datasources using the Datasource custom resource (cr). You can deploy a sample Prometheus datasource for the previously created org using one of the example files.

```
$ kubectl apply -f examples/example.com-grafana-datasource-full-body.yaml
```

You can inspect the contents of the Datasource object and note that:

* It has a list of organizations the datasource belongs to. Handy for when you want the same datasource across many organizations.
* You can specify the name of the datasource and the partial or full JSON body for the datasource.
* Fields orgID and name in the JSON body will be modified by the operator to match the spec.datasource.name and the respective orgId from the spec.organizations list when creating/updating.

```yaml
apiVersion: grafana.k8spin.cloud/v1
kind: Datasource
metadata:
  name: example-graphite-test
spec:
  organizations:
  - example.com
  - great-customer-org
  datasource:
    name: graphite-test
    data: |-
      {
        "id": 1,
        "orgId": 1,
        "name": "test_datasource",
        "type": "graphite",
        "typeLogoUrl": "",
        "access": "proxy",
        "url": "http://mydatasource.test",
        "password": "",
        "user": "",
        "database": "",
        "basicAuth": false,
        "basicAuthUser": "",
        "basicAuthPassword": "",
        "withCredentials": false,
        "isDefault": false,
        "jsonData": {
          "graphiteType": "default",
          "graphiteVersion": "1.1"
        },
        "secureJsonFields": {},
        "version": 1,
        "readOnly": false
      }

```


## Create an Organization Dashboard with a CustomResource

You can create organization Dashboards using the Dashboard cr. Let's go ahead and create the following example dashboard.

```
$ kubectl apply -f examples/example.com-grafana-dashboard.yaml
```

If you inspect the file, you will see the custom resource is composed of 2 important fields:

* A list of organizations to create the dashboard in
* The JSON exported dashboard resource

```yaml
apiVersion: grafana.k8spin.cloud/v1
kind: Dashboard
metadata:
  name: my-fancy-dashboard
spec:
  organizations:
  - example.com
  dashboard:
    name: my-dashboard
    data: |-
      {
      ...
      }
```

You should then see the dashboard populated in the organization folder.

## Create an example User

Create a User

```bash
$ kubectl apply -f examples/example.com-grafana-user.yaml
user.grafana.k8spin.cloud/jhon-doe created
```

Verify the User CR contains an User Organization identifier:

```bash
$ kubectl  describe user jhon-doe
$ echo "Parsing with jq"
"Parsing with jq"
$ kubectl  get user jhon-doe -o json | jq -r .status.create_user.id
2
```

You can also see it at `my_grafana_host` site:

![example.com Organization @ Grafana](../assets/user-list.png)


Edit the User cr adding the user to the example.com organization:

```bash
$ kubectl edit user jhon-doe
user.grafana.k8spin.cloud/jhon-doe edited
$ kubectl get user jhon-doe -o yaml
apiVersion: grafana.k8spin.cloud/v1
kind: User
metadata:
  finalizers:
  - kopf.zalando.org/KopfFinalizerMarker
  name: jhon-doe
  namespace: default
spec:
  email: jhon-doe@example.com
  organizations:
  - example.com
```

Check the User at `my_grafana_host` site:

![Jhon doe](../assets/jhon-doe.png)

Use the user to login at `my_grafana_host` site:

- User: `jhon-doe`
- Password: `changemeplease`

![Jhon doe Login](../assets/jhon-doe-login.png)
![Jhon doe In](../assets/jhon-doe-in.png)

### Clean up

Delete both organization and user

```bash
$ kubectl delete -f examples/example.com-grafana-user.yaml
user.grafana.k8spin.cloud "jhon-doe" deleted
$ kubectl delete -f examples/example.com-grafana-org.yaml
organization.grafana.k8spin.cloud "example.com" deleted
```
