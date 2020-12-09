import json

import asyncio
import kopf

from grafana import api, organization, user, dashboard

ORG_SWITCH_LOCK: asyncio.Lock


@kopf.on.startup()
async def startup_fn(logger, **kwargs):
    global ORG_SWITCH_LOCK
    ORG_SWITCH_LOCK = asyncio.Lock()  # uses the running asyncio loop by default


@kopf.on.create('grafana.k8spin.cloud', 'v1', 'organizations')
async def create_organization(spec, meta, **kwargs):
    name = meta.get('name')
    datasources = spec.get('datasources', list())
    dashboards = spec.get('dashboards', list())
    return await organization.create(api, name, datasources, dashboards, ORG_SWITCH_LOCK)


@kopf.on.update('grafana.k8spin.cloud', 'v1', 'organizations')
async def update_organization(old, new, status, **kwargs):
    orgId = status['create_organization']['orgId']
    oldDataSources = old.get('spec').get('datasources', list())
    newDataSources = new.get('spec').get('datasources', list())
    oldDashboards = old.get('spec').get('dashboards', list())
    newDashboards = new.get('spec').get('dashboards', list())
    await organization.update(api, orgId, oldDataSources,
                              newDataSources, oldDashboards, newDashboards, ORG_SWITCH_LOCK)


@kopf.on.delete('grafana.k8spin.cloud', 'v1', 'organizations')
def delete_organization(status, **kwargs):
    return organization.delete(api, status['create_organization']['orgId'])


@kopf.on.create('grafana.k8spin.cloud', 'v1', 'users')
def create_user(spec, meta, **kwargs):
    name = meta.get('name')
    email = spec.get('email')
    organizationNames = spec.get('organizations', list())
    return user.create(api, name, email, organizationNames)


@kopf.on.update('grafana.k8spin.cloud', 'v1', 'users')
def update_user(status, spec, meta, old, new, **kwargs):
    oldOrganizationNames = old.get('spec').get('organizations', list())
    newOrganizationNames = new.get('spec').get('organizations', list())
    userId = status['create_user']['id']
    name = meta.get('name')
    email = spec.get('email')
    return user.update(api, userId, name, email, oldOrganizationNames, newOrganizationNames)


@kopf.on.delete('grafana.k8spin.cloud', 'v1', 'users')
def delete_user(status, **kwargs):
    return user.delete(api, status['create_user']['id'])


@kopf.on.create('grafana.k8spin.cloud', 'v1', 'dashboards')
def create_dashboard(spec, meta, **kwargs):
    name = meta.get('name')
    jsonDashboard = json.loads(spec.get('jsonDashboard'))
    organizationNames = spec.get('organizations', list())
    return dashboard.create(api, name, jsonDashboard, organizationNames)


@kopf.on.update('grafana.k8spin.cloud', 'v1', 'dashboards')
def update_dashboard(status, spec, meta, old, new, **kwargs):
    name = meta.get('name')
    oldOrganizationNames = old.get('spec').get('organizations', list())
    newOrganizationNames = new.get('spec').get('organizations', list())
    newJsonDashboard = json.loads(new.get('spec').get('jsonDashboard'))
    return dashboard.update(api, name, oldOrganizationNames, newOrganizationNames, newJsonDashboard)


@kopf.on.delete('grafana.k8spin.cloud', 'v1', 'dashboards')
def delete_dashboard(spec, meta, **kwargs):
    organizationNames = spec.get('organizations', list())
    name = meta.get('name')
    return dashboard.delete(api, name, organizationNames)
