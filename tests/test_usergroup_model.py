from .conftest import get_session
import sys
sys.path.append("..")
from db.models import UserGroup
from .seeder import (
    seed_client,
    seed_user_group
)
from schema import UserGroupSchema, UpdateUserGroupSchema
import uuid

def test_create_user_group(get_session):
    # seed the client
    seed_client(get_session)
    # first check that table is empty.
    retrieve_groups = UserGroup.get_user_groups(get_session)
    assert len(retrieve_groups.all()) == 0
    # data to populate the table with
    user_group_data = {
        'group_name': 'admin',
        'slug': 'slug'
    }
    # load for client_id 1
    user_group_data['client_id'] = 1
    
    created_group = UserGroup.create_user_group(user_group_data)
    get_session.add(created_group)
    get_session.commit()
    # check if it was created successfully.
    assert created_group is not None
    retrieve_groups = UserGroup.get_user_groups(get_session)
    assert len(retrieve_groups.all()) == 1
    # get group added, and be sure it tallies.
    get_group = UserGroup.get_client_user_groups(get_session, 1).first()
    assert get_group.client_id == 1
    assert get_group.status == True
    assert get_group.group_name == 'admin'
    assert get_group.slug == 'slug'
    
def test_update_user_group(get_session):
    # seed the client and user_group
    seed_client(get_session)
    seed_user_group(get_session)
    
    #update_group_data
    update_group_data = {
        'status': False
    }
    # get group added, and its data.
    get_group = UserGroup.get_user_group_by_id(get_session, 1)
    assert get_group.client_id == 1
    assert get_group.status == True
    # update the data.
    updated_group = UserGroup.update_user_group(get_session, 
                                                1, update_group_data)
    get_session.commit()
    get_session.refresh(updated_group)    
    # check if it was updated.
    get_group = UserGroup.get_user_group_by_id(get_session, 1)
    assert get_group.client_id == 1
    assert get_group.status == False
    
def test_get_all_groups(get_session):
     # seed the client and user_group
    seed_client(get_session)
    seed_user_group(get_session)
    #update_group_data
    update_group_data = {
        'status': False
    }
    # get all groups added.
    retrieve_groups = UserGroup.get_user_groups(get_session)
    assert len(retrieve_groups.all()) == 4
    
def test_get_all_groups_per_client(get_session):
     # seed the client and user_group
    seed_client(get_session)
    seed_user_group(get_session)
    #update_group_data
    update_group_data = {
        'status': False
    }
    # get all groups added.
    retrieve_groups = UserGroup.get_client_user_groups(get_session, 1)
    assert len(retrieve_groups.all()) == 2
    
    
    
    
    