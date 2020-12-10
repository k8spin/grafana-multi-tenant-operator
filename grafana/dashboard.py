from grafana import MAIN_ORG_ID, organization, GrafanaClientError


async def create(api, name, jsonDashboard, organizationNames, lock, logger):
    responses = []
    orgIds = [organization.find_by_name(api, orgName).get('id')
              for orgName in organizationNames]
    await lock.acquire()
    try:
        for orgId in orgIds:
            api.organizations.switch_organization(orgId)
            jsonDashboard['id'] = None
            # Setting the uid to the resource name, to be able to find it later
            jsonDashboard['uid'] = name
            dashboard_object = {
                'dashboard': jsonDashboard,
                'folderId': 0,
                'overwrite': False
            }
            try:
                response = api.dashboard.update_dashboard(dashboard_object)
                responses.append(response)
            except GrafanaClientError as err:
                logger.error(err)
        api.organizations.switch_organization(MAIN_ORG_ID)
    finally:
        lock.release()
    return responses


async def update(api, name, oldOrganizationNames, newOrganizationNames, newJsonDashboard, lock, logger):
    responses = []
    # Delete dashboards from organizations it doesn't belong
    pruneOrgs = [
        item for item in oldOrganizationNames if item not in newOrganizationNames]
    pruneOrgIds = [organization.find_by_name(api, orgName).get('id')
                   for orgName in pruneOrgs]
    if pruneOrgIds:
        await lock.acquire()
        try:
            for orgId in pruneOrgIds:
                api.organizations.switch_organization(orgId)
                try:
                    api.dashboard.delete_dashboard(name)
                except GrafanaClientError as err:
                    logger.error(err)
        finally:
            lock.release()
    # Update dashboards
    orgIds = [organization.find_by_name(api, orgName).get('id')
              for orgName in newOrganizationNames]
    await lock.acquire()
    try:
        for orgId in orgIds:
            api.organizations.switch_organization(orgId)
            try:
                api.dashboard.delete_dashboard(name)
            except GrafanaClientError as err:
                if err.status_code == 404:
                    logger.debug(
                        f'Dashboard not found for update. Proceeding to create it in org {orgId}.')
                else:
                    logger.error(err)
            newJsonDashboard['id'] = None
            # Setting the uid to the resource name, to be able to find it later
            newJsonDashboard['uid'] = name
            dashboard_object = {
                'dashboard': newJsonDashboard,
                'folderId': 0,
                'overwrite': False
            }
            responses.append(api.dashboard.update_dashboard(dashboard_object))
        api.organizations.switch_organization(MAIN_ORG_ID)
    finally:
        lock.release()
    return responses


async def delete(api, name, organizationNames, lock, logger):
    responses = []
    orgIds = [organization.find_by_name(api, orgName).get('id')
              for orgName in organizationNames]
    await lock.acquire()
    try:
        for orgId in orgIds:
            api.organizations.switch_organization(orgId)
            try:
                api.dashboard.delete_dashboard(name)
            except GrafanaClientError as err:
                logger.error(err)
        api.organizations.switch_organization(MAIN_ORG_ID)
    finally:
        lock.release()
    return responses
