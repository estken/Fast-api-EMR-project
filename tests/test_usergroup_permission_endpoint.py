from .conftest import get_session, client_instance, admin_login
import sys
sys.path.append("..")
from db.client_model import UserGroupPermission, UserGroup, Permissions
from .seeder import(
    seed_user_group,
    seed_permission,
    seed_group_permission
)

import logging

# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

def test_add_user_group_permission(get_session, client_instance, admin_login):
    # add the usergroup data.
    user_group_data = UserGroup(**{
        'slug':'new_slug', 'group_name': 'new_group', 'id': 100
    })
    get_session.add(user_group_data)
    get_session.commit()
    # add the permission data.
    permission_data = Permissions(**{
        'id': 100, 'router_name': 'new_router', 'description': 'desc6', 'label': 'new router'
    })
    get_session.add(permission_data)
    get_session.commit()
    
    # check that the user group permission model does not contain any permission for the usergroup.
    user_group_permission = get_session.query(UserGroupPermission).filter_by(
        user_group_id=100).all()
    assert len(user_group_permission) == 0
    # data to be added. The data is already present in both the user group and permission as well.
    user_permit_data = {
        'router_name': 'new_router',
        'group_slug':  'new_slug'
    }
     # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # add the usergroup permission.
    user_permit_response = client_instance.post('/user/group/permission/add', json=user_permit_data, headers=headers)
    assert user_permit_response.status_code == 201
    assert user_permit_response.json()['status'] == 1
    # check to be sure that the data is added properly.
    assert len(get_session.query(UserGroupPermission).filter_by(user_group_id=100).all()) == 1
    get_permit = get_session.query(UserGroupPermission).filter(UserGroupPermission.user_group_id==100).first()
    assert get_permit.user_group.slug == user_permit_data['group_slug']
    assert get_permit.permissions.router_name == user_permit_data['router_name']

def test_add_user_group_permission_error(get_session, client_instance, admin_login):
    # check that the model is empty.
    user_group_permission = get_session.query(UserGroupPermission).all()
    assert len(user_group_permission) == 0
    # seed the user group and user permission.
    seed_user_group(get_session)
    seed_permission(get_session)
    # try adding wrong data.
    user_permit_data = {
        'router_name': 'router18',
        'group_slug':  'slug4'
    }
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # add the usergroup permission.
    user_permit_response = client_instance.post('/user/group/permission/add', json=user_permit_data, headers=headers)
    assert user_permit_response.status_code == 400
    assert user_permit_response.json()['status'] == 0
    
def test_all_user_group_permit(get_session, client_instance, admin_login):
    # seed all the data.
    seed_user_group(get_session)
    seed_permission(get_session)
    seed_group_permission(get_session)
    
    all_user_permit = get_session.query(UserGroupPermission).filter_by(user_group_id=1).all()
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    user_permit_response = client_instance.get('/user/group/permission/slug', headers=headers)
    assert len(user_permit_response.json()['data']) == len(all_user_permit)


def test_remove_user_permit(get_session, client_instance, admin_login):
    # seed all the data.
    # add the usergroup data.
    user_group_data = UserGroup(**{
        'slug':'new_slug', 'group_name': 'new_group', 'id': 100
    })
    get_session.add(user_group_data)
    get_session.commit()
    # add the permission data.
    permission_data = Permissions(**{
        'id': 100, 'router_name': 'new_router', 'description': 'desc6', 'label': 'new router'
    })
    get_session.add(permission_data)
    get_session.commit()
    
    # check that the user group permission model does not contain any permission for the usergroup.
    user_group_permission = get_session.query(UserGroupPermission).filter_by(
        user_group_id=100).all()
    assert len(user_group_permission) == 0
    # add the new permission for the usergroup.
    user_group_permit = UserGroupPermission(**{
        'user_group_id': 100, 'permission_id': 100
    })
    get_session.add(user_group_permit)
    get_session.commit()
    # ensure it was added.
    initial_user_permit = get_session.query(UserGroupPermission).filter_by(user_group_id=100).all()
    assert len(initial_user_permit) == 1
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # delete the newly added permission for the new user group.
    user_permit_data = {
        'route_names': ['new_router1'],
    }
    
    user_permit_response = client_instance.delete('/user/group/permission/remove/new_slug', params=user_permit_data, headers=headers)
    get_session.commit()
    all_user_permit_deleted = get_session.query(UserGroupPermission).filter_by(user_group_id=1).all()
    assert len(all_user_permit_deleted) == (len(initial_user_permit) - 1)