from .conftest import get_session
import sys
sys.path.append("..")
from db import client_model as models
from .seeder import (
    seed_client,
    seed_user_group
)
from schema import UserGroupSchema, UpdateUserGroupSchema
import uuid

def test_create_user_group(get_session):
    # first check that table is empty.
    retrieve_groups = models.UserGroup.get_user_groups(get_session)
    assert len(retrieve_groups.all()) == 0
    # data to populate the table with
    user_group_data = {
        'group_name': 'admin',
        'slug': 'slug'
    }
    
    created_group = models.UserGroup.create_user_group(user_group_data)
    get_session.add(created_group)
    get_session.commit()
    # check if it was created successfully.
    assert created_group is not None
    retrieve_groups = models.UserGroup.get_user_groups(get_session)
    assert len(retrieve_groups.all()) == 1
    # get group added, and be sure it tallies.
    get_group = models.UserGroup.get_user_group_by_id(get_session, 1)
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
    get_group = models.UserGroup.get_user_group_by_id(get_session, 1)
    assert get_group.status == True
    # update the data.
    updated_group = models.UserGroup.update_user_group(get_session, 
                                                1, update_group_data)
    get_session.commit()
    get_session.refresh(updated_group)    
    # check if it was updated.
    get_group = models.UserGroup.get_user_group_by_id(get_session, 1)
    assert get_group.status == False
    
def test_get_all_groups(get_session):
     # seed the client and user_group
    seed_client(get_session)
    seed_user_group(get_session)
    # get all groups added.
    retrieve_groups = models.UserGroup.get_user_groups(get_session)
    assert len(retrieve_groups.all()) == 18
    
    
    
    