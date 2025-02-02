from .conftest import get_session
import sys
sys.path.append("..")
from db import client_model as models
from schema import ClientUserSchema, UpdateClientUserSchema
import uuid
from .seeder import seed_client, seed_client_users, seed_client_center

def test_create_user(get_session):
    # seed the client.
    seed_client(get_session)
    seed_client_center(get_session)
    # create the data.
    user_data = {
        "username": "abc@gmail.com",
        "password": "admin@123",
        "client_id": 1
    }
    # first check if the model is empty.
    retrieve_users = models.ClientUsers.retrieve_all_users(get_session)
    assert len(retrieve_users.all()) == 0
    # add the data.
    new_user = models.ClientUsers.create_client_users(user_data)
    get_session.add(new_user)
    get_session.commit()
    # check if it was added.
    get_users =  models.ClientUsers.retrieve_all_users(get_session)
    assert len(get_users.all()) == 1
    # check the username address to be sure the list tallies.
    check_user = models.ClientUsers.check_client_username(get_session, 1, 'abc@gmail.com')
    assert check_user.admin == False
    assert check_user.username == "abc@gmail.com"
    assert check_user.client_id == 1
    
def test_retrieve_all_users(get_session):
    seed_client(get_session)
    seed_client_users(get_session)
    # get all the users
    get_users =  models.ClientUsers.retrieve_all_users(get_session)
    assert len(get_users.all()) == 2
    
def test_retrieve_users_per_client(get_session):
    seed_client(get_session)
    seed_client_users(get_session)
    # get users per client.
    get_users =  models.ClientUsers.retrieve_client_users(get_session, 1)
    assert len(get_users.all()) == 1
    
def test_update_client_user(get_session):
    seed_client(get_session)
    seed_client_users(get_session)
    # create the update data.
    update_data = {
        'admin': False,
        'username': 'aa@gmail.com'
    }
    # check the data before it was updated.
    get_user = models.ClientUsers.retrieve_user_by_id(get_session, 1)
    assert get_user is not None
    assert get_user.admin == True
    assert get_user.username == "admin@intuitive.com"
    # now update.
    update_schema = UpdateClientUserSchema(**update_data)
    update_user = models.ClientUsers.update_client_user(
        get_session, 1, update_schema.dict(exclude_unset=True))
    get_session.commit()
    get_session.refresh(update_user)
    # check the data after it has been updated.
    get_user = models.ClientUsers.retrieve_user_by_id(get_session, 1)
    assert get_user is not None
    assert get_user.admin == False
    assert get_user.username == "aa@gmail.com"