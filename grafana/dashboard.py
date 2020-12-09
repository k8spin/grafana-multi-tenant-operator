from grafana import MAIN_ORG_ID, organization


def create(api, name, jsonDashboard, organizationNames):
    responses = []
    orgIds = [organization.find_by_name(api, orgName).get('id')
              for orgName in organizationNames]
    for orgId in orgIds:
        api.organizations.switch_organization(orgId)
        # Removing id field from the dashboard JSON
        del jsonDashboard['id']
        # Setting the uid to the resource name, to be able to find it later
        jsonDashboard['uid'] = name
        dashboard_object = {
            'dashboard': jsonDashboard,
            'folderId': 0,
            'overwrite': False
        }
        responses.append(api.dashboard.update_dashboard(dashboard_object))
    api.organizations.switch_organization(MAIN_ORG_ID)
    return responses


def update(api, name, oldOrganizationNames, newOrganizationNames, newJsonDashboard):
    responses = []
    # Delete dashboards from organizations it doesn't belong
    pruneOrgs = [
        item for item in oldOrganizationNames if item not in newOrganizationNames]
    pruneOrgIds = [organization.find_by_name(api, orgName).get('id')
                   for orgName in pruneOrgs]
    if pruneOrgIds:
        for orgId in pruneOrgIds:
            api.organizations.switch_organization(orgId)
            responses.append(api.dashboard.delete_dashboard(name))
    # Update dashboards
    orgIds = [organization.find_by_name(api, orgName).get('id')
              for orgName in newOrganizationNames]
    for orgId in orgIds:
        api.organizations.switch_organization(orgId)
        api.dashboard.delete_dashboard(name)
        # Removing id field from the dashboard JSON
        del newJsonDashboard['id']
        # Setting the uid to the resource name, to be able to find it later
        newJsonDashboard['uid'] = name
        dashboard_object = {
            'dashboard': newJsonDashboard,
            'folderId': 0,
            'overwrite': False
        }
        responses.append(api.dashboard.update_dashboard(dashboard_object))
    api.organizations.switch_organization(MAIN_ORG_ID)
    return responses


def delete(api, name, organizationNames):
    responses = []
    orgIds = [organization.find_by_name(api, orgName).get('id')
              for orgName in organizationNames]
    for orgId in orgIds:
        api.organizations.switch_organization(orgId)
        api.dashboard.delete_dashboard(name)
    api.organizations.switch_organization(MAIN_ORG_ID)
    return responses
