from grafana import MAIN_ORG_ID, GrafanaException, organization


async def create(api, name, jsonDashboard, organizationNames, lock, logger):
    responses = []
    orgIds = []
    try:
        orgIds = [organization.find_by_name(api, orgName).get('id')
                  for orgName in organizationNames]
    except GrafanaException as err:
        logger.error(
            f'Something went wrong when trying to lookup an organization by name: {err}')
    await lock.acquire()
    try:
        for orgId in orgIds:
            try:
                api.organizations.switch_organization(orgId)
                jsonDashboard['uid'] = name
                jsonDashboard['title'] = name
                del jsonDashboard['id']
                dashboard_object = {
                    'dashboard': jsonDashboard,
                    'folderId': 0,
                    'overwrite': False
                }
                response = api.dashboard.update_dashboard(dashboard_object)
                responses.append(response)
            except GrafanaException as err:
                logger.error(
                    f'Unable to create dashboard with name {name} in organization {orgId}: {err}')
        api.organizations.switch_organization(MAIN_ORG_ID)
    finally:
        lock.release()
    return responses


async def update(api, oldName, newName, oldOrganizationNames, newOrganizationNames, jsonDashboard, lock, logger):
    responses = []
    # Delete dashboards from organizations it doesn't belong
    pruneOrgs = [
        item for item in oldOrganizationNames if item not in newOrganizationNames]
    pruneOrgIds = []
    try:
        pruneOrgIds = [organization.find_by_name(api, orgName).get('id')
                       for orgName in pruneOrgs]
    except GrafanaException as err:
        logger.error(
            f'Unable to get organization by name in update dashboard: {err}')
    if pruneOrgIds:
        await lock.acquire()
        try:
            for orgId in pruneOrgIds:
                api.organizations.switch_organization(orgId)
                try:
                    api.dashboard.delete_dashboard(oldName)
                except GrafanaException as err:
                    logger.error(
                        f'Unable to prune dashboard with uid {oldName} in organization {orgId}: err')
        finally:
            lock.release()
    # Update dashboards
    orgIds = []
    try:
        orgIds = [organization.find_by_name(api, orgName).get('id')
                  for orgName in newOrganizationNames]
    except GrafanaException as err:
        logger.error(
            f'Something went wrong when trying to lookup an organization by name: {err}')
    await lock.acquire()
    try:
        for orgId in orgIds:
            try:
                api.organizations.switch_organization(orgId)
            except GrafanaException as err:
                logger.error(
                    f'Unable to switch to organization with id={orgId}: {err}')
            try:
                api.dashboard.delete_dashboard(oldName)
            except GrafanaException as err:
                if err.status_code == 404:
                    logger.debug(
                        f'Dashboard not found for update. Proceeding to create it in org {orgId}.')
                else:
                    logger.error(
                        f'Something went wrong when trying to delete dashboard {oldName} in org {orgId}: {err}')
            jsonDashboard['id'] = None
            # Setting the uid to the resource name, to be able to find it later
            jsonDashboard['uid'] = newName
            dashboard_object = {
                'dashboard': jsonDashboard,
                'folderId': 0,
                'overwrite': False
            }
            try:
                responses.append(
                    api.dashboard.update_dashboard(dashboard_object))
            except GrafanaException as err:
                logger.error(
                    f'Something went wrong when trying to create dashboard {newName} in org {orgId}: {err}')
        api.organizations.switch_organization(MAIN_ORG_ID)
    finally:
        lock.release()
    return responses


async def delete(api, name, organizationNames, lock, logger):
    responses = []
    orgIds = []
    try:
        orgIds = [organization.find_by_name(api, orgName).get('id')
                  for orgName in organizationNames]
    except GrafanaException as err:
        logger.error(
            f'Something went wrong when trying to lookup an organization by name: {err}')
    await lock.acquire()
    try:
        for orgId in orgIds:
            try:
                api.organizations.switch_organization(orgId)
                responses.append(api.dashboard.delete_dashboard(name))
            except GrafanaException as err:
                logger.error(
                    f'Unable to delete the dashboard with name {name} in organization {orgId}: {err}')
        api.organizations.switch_organization(MAIN_ORG_ID)
    finally:
        lock.release()
    return responses
