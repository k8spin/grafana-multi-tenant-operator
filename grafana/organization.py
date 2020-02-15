import json

from grafana import MAIN_ORG_ID


def create(api, name, dataSources, dashboards):
    response = api.organization.create_organization({'name': name})
    _create_datasources(api, dataSources, response.get('orgId'))
    _create_dashboards(api, dashboards, response.get('orgId'))
    return response


def update(api, orgId, oldDataSources, newDataSources, oldDashboards, newDashboards):
    _delete_datasources(api, oldDataSources, orgId)
    _create_datasources(api, newDataSources, orgId)
    _delete_dashboards(api, oldDashboards, orgId)
    _create_dashboards(api, newDashboards, orgId)


def delete(api, orgId):
    return api.organizations.delete_organization(orgId)


def find_by_name(api, name):
    return api.organization.find_organization(name)


def _create_datasources(api, dataSources, orgId):
    api.organizations.switch_organization(orgId)
    for dataSource in dataSources:
        dataSourceName = dataSource.get('name')
        dataSourceParsed = json.loads(dataSource.get('data'))
        # Override the name
        dataSourceParsed['name'] = dataSourceName
        api.datasource.create_datasource(dataSourceParsed)
    api.organizations.switch_organization(MAIN_ORG_ID)


def _create_dashboards(api, dashboards, orgId):
    api.organizations.switch_organization(orgId)
    for dashboard in dashboards:
        dashboardName = dashboard.get('name')
        dashboardParsed = json.loads(dashboard.get('data'))
        # Override the uid and title
        dashboardParsed['uid'] = dashboardName
        dashboardParsed['title'] = dashboardName
        del dashboardParsed['id']
        dashboard_object = {
            'dashboard': dashboardParsed,
            'folderId': 0,
            'overwrite': False
        }
        api.dashboard.update_dashboard(dashboard_object)
    api.organizations.switch_organization(MAIN_ORG_ID)


def _delete_datasources(api, dataSources, orgId):
    api.organizations.switch_organization(orgId)
    for dataSource in dataSources:
        api.datasource.delete_datasource_by_name(dataSource.get('name'))
    api.organizations.switch_organization(MAIN_ORG_ID)


def _delete_dashboards(api, dashboards, orgId):
    api.organizations.switch_organization(orgId)
    for dashboard in dashboards:
        api.dashboard.delete_dashboard(dashboard.get('name'))
    api.organizations.switch_organization(MAIN_ORG_ID)
