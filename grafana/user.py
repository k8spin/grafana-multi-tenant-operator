from grafana import MAIN_ORG_ID, organization


def create(api, name, email, organizationNames):
    response = api.admin.create_user({
        'name': name,
        'email': email,
        'login': name,
        'password': 'changemeplease'
    })
    userId = response.get('id')
    revokeOrgs = [MAIN_ORG_ID]
    orgIds = [organization.find_by_name(api, orgName).get('id')
              for orgName in organizationNames]
    _revoke_organizations(api, userId, revokeOrgs)
    _add_organizations(api, name, orgIds)
    return response


def update(api, userId, name, email, oldOrganizationNames, newOrganizationNames):
    response = api.users.update_user(userId, {
        'email': email,
        'name': name,
        'login': name
    })
    revokeOrgs = [organization.find_by_name(api, orgName).get('id')
                  for orgName in oldOrganizationNames]
    orgIds = [organization.find_by_name(api, orgName).get('id')
              for orgName in newOrganizationNames]
    _revoke_organizations(api, userId, revokeOrgs)
    _add_organizations(api, name, orgIds)
    return response


def delete(api, userId):
    return api.admin.delete_user(userId)


def _add_organizations(api, name, orgIds):
    _data = {
        'loginOrEmail': name,
        'role': 'Viewer'
    }
    for orgId in orgIds:
        api.organizations.organization_user_add(orgId, _data)


def _revoke_organizations(api, userId, orgIds):
    for orgId in orgIds:
        api.organizations.organization_user_delete(orgId, userId)
