from .conftest import get_session, client_instance, admin_login
import sys
sys.path.append("..")
from db import client_model as models
from schema import UserGroupSchema, UpdateUserGroupSchema
from fastapi import status
from .seeder import(
    seed_client,
    seed_user_group
)

import logging

# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

def test_create_user_group(client_instance, admin_login):
    # Create a user group with the given name and slug
    user_group_data = {
        'group_name': 'group_name1'
    }
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # create the group
    group_response = client_instance.post('/user/group/create', json=user_group_data, headers=headers)
    assert group_response.status_code == 201
    assert group_response.json()['detail'] == "UserGroup was successfully created"
    assert group_response.json()['status'] == 1
    
def test_create_user_group_exist_error(client_instance, get_session, admin_login):
    # seed client and usergroup
    seed_client(get_session)
    seed_user_group(get_session)
    # Create a user group with the given name and slug
    user_group_data = {
        'group_name': 'admin'
    }
    # header.
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # create the group
    group_response = client_instance.post('/user/group/create', json=user_group_data, headers=headers)
    assert group_response.status_code == 400
    assert group_response.json()['detail'] == f"Sorry, User Group with group name {user_group_data['group_name']} exists for this client"
    assert group_response.json()['status'] == 0
    
    
def test_disable_group(client_instance, get_session, admin_login):
    # Seeding data into database before testing deactivate function
    seed_client(get_session)
    seed_user_group(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # check the status of the user group.
    get_group = models.UserGroup.get_user_group_by_id(get_session, 1)
    assert get_group.status == True
    # deactivate.
    group_response = client_instance.patch('/user/group/disable/slug', headers=headers)
    get_session.commit()
    assert group_response.status_code == 200
     # check the status of the user group.
    get_group = models.UserGroup.get_user_group_by_id(get_session, 1)
    assert get_group.status == False
        
def test_view_all_groups(client_instance, get_session, admin_login):
    # seed the database for client and user_group tables.
    seed_client(get_session)
    seed_user_group(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    
    # with default length 10
    group_response = client_instance.get('/user/group/', headers=headers)
    assert len(group_response.json()['data']['items']) == 10
    assert group_response.status_code == 200
    assert group_response.json()['data']['page'] == 1
    
    
def test_view_all_groups_without_size(client_instance, get_session, admin_login):
    # seed the database for client and user_group tables.
    seed_client(get_session)
    seed_user_group(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # with default length 10
    group_response = client_instance.get('/user/group/', headers=headers)
    assert len(group_response.json()['data']['items']) == 10
    assert group_response.status_code == 200
    assert group_response.json()['data']['page'] == 1
    
def test_view_all_groups_with_size(client_instance, get_session, admin_login):
    # seed the database for client and user_group tables.
    seed_client(get_session)
    seed_user_group(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # with default length 10
    group_response = client_instance.get('/user/group/', headers=headers, params={"page":1, "page_size":3})
    assert len(group_response.json()['data']['items']) == 3
    assert group_response.status_code == 200
    assert group_response.json()['data']['page'] == 1
    
def test_view_single_groups(client_instance, get_session, admin_login):
    # seed the database for client and user_group tables.
    seed_client(get_session)
    seed_user_group(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # with default length 10
    group_response = client_instance.get('/user/group/single/slug', headers=headers)
    assert group_response.status_code == 200    