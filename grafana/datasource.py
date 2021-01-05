from grafana import MAIN_ORG_ID, GrafanaException, organization


async def create(api, name, jsonDatasource, organizationNames, lock, logger):
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
                jsonDatasource['name'] = name
                if jsonDatasource.get('id'):
                    del jsonDatasource['id']
                response = api.datasource.create_datasource(jsonDatasource)
                responses.append(response)
            except GrafanaException as err:
                logger.error(
                    f'Unable to create datasource with name {name} in organization {orgId}: {err}')
        api.organizations.switch_organization(MAIN_ORG_ID)
    finally:
        lock.release()
    return responses


async def update(api, oldName, newName, newJsonDatasource, oldOrganizationNames, newOrganizationNames, lock, logger):
    responses = []
    # Delete the datasource from organizations it doesn't belong
    pruneOrgs = [
        item for item in oldOrganizationNames if item not in newOrganizationNames]
    pruneOrgIds = []
    try:
        pruneOrgIds = [organization.find_by_name(api, orgName).get('id')
                       for orgName in pruneOrgs]
    except GrafanaException as err:
        logger.error(
            f'Unable to get organization by name in update datasource: {err}')
    if pruneOrgIds:
        await lock.acquire()
        try:
            for orgId in pruneOrgIds:
                api.organizations.switch_organization(orgId)
                try:
                    api.datasource.delete_datasource_by_name(
                        oldName)
                except GrafanaException as err:
                    logger.error(
                        f'Unable to prune datasource with name {oldName} in organization {orgId}: {err}')
            api.organizations.switch_organization(MAIN_ORG_ID)
        finally:
            lock.release()
    # Recreate datasource for orgs that retain the datasource
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
            api.organizations.switch_organization(orgId)
            try:
                api.datasource.delete_datasource_by_name(oldName)
            except GrafanaException as err:
                logger.error(
                    f'Unable to delete datasource with name {newName} in organization {orgId}: {err}')
            try:
                newJsonDatasource['name'] = newName
                if newJsonDatasource.get('id'):
                    del newJsonDatasource['id']
                response = api.datasource.create_datasource(newJsonDatasource)
                responses.append(response)
            except GrafanaException as err:
                logger.error(
                    f'Unable to create datasource with name {newName} in organization {orgId}: {err}')
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
            api.organizations.switch_organization(orgId)
            try:
                response = api.datasource.delete_datasource_by_name(
                    name)
                responses.append(response)
            except GrafanaException as err:
                logger.error(
                    f'Unable to prune datasource with name {name} in organization {orgId}: {err}')
        api.organizations.switch_organization(MAIN_ORG_ID)
    finally:
        lock.release()
    return responses
