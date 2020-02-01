import json

from grafana import MAIN_ORG_ID


def create(api, name, dataSources):
    response = api.organization.create_organization({'name': name})
    _create_datasources(api, dataSources, response.get('orgId'))
    return response


def update(api, orgId, oldDataSources, newDataSources):
    _delete_datasources(api, oldDataSources, orgId)
    _create_datasources(api, newDataSources, orgId)


def delete(api, orgId):
    return api.organizations.delete_organization(orgId)


def find_by_name(api, name):
    return api.organization.find_organization(name)


def _create_datasources(api, dataSources, orgId):
    api.organizations.switch_organization(orgId)
    for dataSource in dataSources:
        dataSourceName = dataSource.get('name')
        dataSourceParsed = json.loads(dataSource.get('ds'))
        # Override the name
        dataSourceParsed['name'] = dataSourceName
        api.datasource.create_datasource(dataSourceParsed)
    api.organizations.switch_organization(MAIN_ORG_ID)


def _delete_datasources(api, dataSources, orgId):
    api.organizations.switch_organization(orgId)
    for dataSource in dataSources:
        api.datasource.delete_datasource_by_name(dataSource.get('name'))
    api.organizations.switch_organization(MAIN_ORG_ID)
