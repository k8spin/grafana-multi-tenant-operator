# Grafana Multi-Tenant Operator Helm Chart

The following table lists the configurable parameters of the `grafana-multi-tenant-operator` chart and their default values.

| Parameter                    | Description                                                                            | Default                                  |
| ---------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------- |
| `replicaCount`               | The number of operator replicas to deploy.                                             | `1`                                      |
| `image.repository`           | The image repository to use with the operator deployment.                              | `"k8spin/grafana-multi-tenant-operator"` |
| `image.pullPolicy`           | Container image pull policy for the deployment.                                        | `"IfNotPresent"`                         |
| `image.tag`                  | Image tag for the operator deployment. Defaults to the appVersion in the `Chart.yaml`. | `""`                                     |
| `imagePullSecrets`           | Secret to use when using private image registries.                                     | `[]`                                     |
| `nameOverride`               | Override the chart naming scheme.                                                      | `""`                                     |
| `fullnameOverride`           | Override the full chart naming scheme.                                                 | `""`                                     |
| `serviceAccount.create`      | Create a Kubernetes service account to be used by the operator.                        | `true`                                   |
| `serviceAccount.annotations` | Annotations to the created Kubernetes service account.                                 | `{}`                                     |
| `serviceAccount.name`        | Provide a specific name for the service account.                                       | `""`                                     |
| `operatorSecretName`         | The name of the secret where the Grafana instance and credentials are located in.      | `"grafana-multi-tenant-operator"`        |
| `podAnnotations`             | Additional pod annotations to the operator.                                            | `{}`                                     |
| `podSecurityContext`         | Provide specific PodSecurityContext to the operator.                                   | `{}`                                     |
| `securityContext`            | Provide specific SecurityContext to the operator.                                      | `{}`                                     |
| `resources`                  | Provide resource requests and resource limits for the operator pods.                   | `{}`                                     |
| `nodeSelector`               | Specify the node selector for the operator.                                            | `{}`                                     |
| `tolerations`                | Provide node tolerations for the operator.                                             | `[]`                                     |
| `affinity`                   | Provide affinity rules to the operator deployment.                                     | `{}`                                     |