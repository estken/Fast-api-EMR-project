from .conftest import get_session, client_instance, admin_login
import sys
sys.path.append("..")
from db.client_model import Permissions
from .seeder import(
    seed_permission
)

import logging

# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

def test_create_permit(get_session, client_instance, admin_login):
    # first check that it is empty.
    get_permissions = get_session.query(Permissions).all()
    assert len(get_permissions) == 0
    # Create a user group with the given name and slug
    permit_data = {
        'router_name': 'router1',
        'description': 'description1',
        'label': 'router 1'
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
    
    get_permissions = get_session.query(Permissions).all()
    assert len(get_permissions) == 1
    # check if it was added.
    added_permission = get_session.query(Permissions).filter_by(router_name=permit_data['router_name']).first()
    assert added_permission.status is True
    assert added_permission.label == permit_data['label']
    assert added_permission.description == permit_data['description']
    
    
def test_disable_permission(get_session, client_instance, admin_login):
    permit_data = {
        'router_name': 'router1',
        'description': 'description1',
        'label': 'router 1'
    }
    new_permit = Permissions(**permit_data)
    get_session.add(new_permit)
    get_session.commit()
    # check if it was added.
    added_permission = get_session.query(Permissions).filter_by(router_name=permit_data['router_name']).first()
    assert added_permission.status is True
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    permit_response = client_instance.patch(f'/permission/disable/{added_permission.router_name}', headers=headers)
    get_session.commit()
    # check if it was disabled.
    updated_permission = get_session.query(Permissions).filter_by(router_name=permit_data['router_name']).first()
    assert updated_permission.status is False
    
def test_enable_permission(get_session, client_instance, admin_login):
    permit_data = {
        'router_name': 'router1',
        'description': 'description1',
        'label': 'router 1',
        'status': False
    }
    new_permit = Permissions(**permit_data)
    get_session.add(new_permit)
    get_session.commit()
    # check if it was added.
    added_permission = get_session.query(Permissions).filter_by(router_name=permit_data['router_name']).first()
    assert added_permission.status is False
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    permit_response = client_instance.patch(f'/permission/enable/{added_permission.router_name}', headers=headers)
    get_session.commit()
    # check if it was disabled.
    updated_permission = get_session.query(Permissions).filter_by(router_name=permit_data['router_name']).first()
    assert updated_permission.status is True
    
    
def test_update_permission(get_session, client_instance, admin_login):
    permit_data = {
        'router_name': 'router1',
        'description': 'old description',
        'label': 'router 1'
    }
    new_permit = Permissions(**permit_data)
    get_session.add(new_permit)
    get_session.commit()
    # check if it was added correctl with the right data.
    added_permission = get_session.query(Permissions).filter_by(router_name=permit_data['router_name']).first()
    assert added_permission.status is True
    assert added_permission.description == "old description"
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # update data
    permit_update_data = {
        "description": "new description"
    }
    
    permit_response = client_instance.patch(f'/permission/update/{added_permission.router_name}', json=permit_update_data, headers=headers)
    get_session.commit()
    # check if it was updated
    updated_permission = get_session.query(Permissions).filter_by(router_name=permit_data['router_name']).first()
    assert updated_permission.status == True
    assert updated_permission.description == "new description"
    
def test_get_all_permission(get_session, client_instance, admin_login):
    seed_permission(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # get all the permission.
    all_permissions = get_session.query(Permissions).all()
    
    permit_response = client_instance.get('/permission/', headers=headers)
    assert len(permit_response.json()['data']['items']) == len(all_permissions)
    assert permit_response.status_code == 200
    assert permit_response.json()['data']['page'] == 1
    
def test_get_active_permission(get_session, client_instance, admin_login):
    seed_permission(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # get all active permissions.
    all_active_permissions = get_session.query(Permissions).filter(Permissions.status==True).all()
    permit_response = client_instance.get('/permission/enabled', headers=headers)
    assert len(permit_response.json()['data']['items']) == len(all_active_permissions)
    assert permit_response.status_code == 200
    assert permit_response.json()['data']['page'] == 1