from .conftest import get_session, client_instance, admin_login
import sys
sys.path.append("..")
from db import client_model as models
from .seeder import(
    seed_permission
)

import logging

# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

def test_create_permit(get_session, client_instance, admin_login):
    # first check that it is empty.
    get_permissions = models.Permissions.get_all_permission(get_session)
    assert len(get_permissions) == 0
    # Create a user group with the given name and slug
    permit_data = {
        'router_name': 'router1',
        'description': 'description1'
    }
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # create the group
    permit_response = client_instance.post('/permission/create', json=permit_data, headers=headers)
    assert permit_response.status_code == 201
    assert permit_response.json()['detail'] == "Permission was successfully created"
    assert permit_response.json()['status'] == 1
    
    get_permissions = models.Permissions.get_all_permission(get_session)
    assert len(get_permissions) == 1
    
def test_disable_permission(get_session, client_instance, admin_login):
    seed_permission(get_session)
    all_permit = models.Permissions.get_all_permission(get_session)
    assert len(all_permit) == 4
    check_permit = models.Permissions.get_permission_by_id(get_session, 1)
    assert check_permit.id == 1
    assert check_permit.status == True
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    
    permit_response = client_instance.patch(f'/permission/disable/{check_permit.router_name}', headers=headers)
    get_session.commit()
    
    check_permit = models.Permissions.get_permission_by_id(get_session, 1)
    assert check_permit.id == 1
    assert check_permit.status == False
    
def test_enable_permission(get_session, client_instance, admin_login):
    seed_permission(get_session)
    check_permit = models.Permissions.get_permission_by_id(get_session, 4)
    assert check_permit.id == 4
    assert check_permit.status == False
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    
    permit_response = client_instance.patch(f'/permission/enable/{check_permit.router_name}', headers=headers)
    get_session.commit()
    
    check_permit = models.Permissions.get_permission_by_id(get_session, 4)
    assert check_permit.id == 4
    assert check_permit.status == True
    
    
def test_update_permission(get_session, client_instance, admin_login):
    seed_permission(get_session)
    check_permit = models.Permissions.get_permission_by_id(get_session, 1)
    assert check_permit.id == 1
    assert check_permit.status == True
    assert check_permit.description == "desc1"
    
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # update data
    permit_update_data = {
        "description": "new description"
    }
    
    permit_response = client_instance.patch(f'/permission/update/{check_permit.router_name}', json=permit_update_data, headers=headers)
    get_session.commit()
    
    check_permit = models.Permissions.get_permission_by_id(get_session, 1)
    assert check_permit.id == 1
    assert check_permit.status == True
    assert check_permit.description == "new description"
    
def test_get_all_permission(get_session, client_instance, admin_login):
    seed_permission(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    
    permit_response = client_instance.get('/permission/', headers=headers)
    assert len(permit_response.json()['data']['items']) == 4
    assert permit_response.status_code == 200
    assert permit_response.json()['data']['page'] == 1
    
def test_get_active_permission(get_session, client_instance, admin_login):
    seed_permission(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    
    permit_response = client_instance.get('/permission/enabled', headers=headers)
    assert len(permit_response.json()['data']['items']) == 3
    assert permit_response.status_code == 200
    assert permit_response.json()['data']['page'] == 1
    

    
    
