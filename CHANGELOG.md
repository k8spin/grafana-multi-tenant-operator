# Changelog

## Version v1.1.0

The second release does not add any functionality to the Operator, but it includes:

- Moved away from GitLab and DockerHub. Hola GitHub!
  - Configured GitHub action to publish container image and the Helm chart. Thanks to @unitygilles
- Configured `bumpversion`.
- Update `python` from `3.7` to `3.9`.
- Update `grafana-api` python dependency.


## Version v1.0.0

This is the first release of Grafana multi-tenant Operator. It includes the following features:

- Organization Management.
    - create, modify, delete organizations.
    - datasources management
    - dashboard management
- User Management
    - Link users to organization
