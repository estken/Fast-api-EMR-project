from .conftest import get_session, client_instance, admin_login
import sys
sys.path.append("..")
from db.client_model import GenderModel
from .seeder import (
    seed_gender
)
from fastapi import status

import logging

# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

def test_create_gender(get_session, client_instance, admin_login):
    # Create a user group with the given name and slug
    gender_data = {
        'name': 'male'
    }
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # check if there is a record with that name first.
    check_gender = get_session.query(GenderModel).filter_by(name=gender_data['name']).first()
    assert check_gender is None
    # create the group
    group_response = client_instance.post('/gender/create', json=gender_data, headers=headers)
    assert group_response.status_code == 201
    assert group_response.json()['detail'] == "Gender was successfully created"
    assert group_response.json()['status'] == 1
    # check if it correctly added.
    added_gender = get_session.query(GenderModel).filter_by(name=gender_data['name']).first()
    assert added_gender.status is True
    assert added_gender.slug is not None
    
def test_create_gender_exist_error(client_instance, get_session, admin_login):
    new_gender_data = {
        'name': 'male',
        'slug': 'slug',
        'status': True
    } 
    new_gender = GenderModel(**new_gender_data)
    get_session.add(new_gender)
    get_session.commit()
    # Create a user group with the given name and slug
    gender_data = {
        'name': 'male'
    }
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # create the group
    group_response = client_instance.post('/gender/create', json=gender_data, headers=headers)
    assert group_response.status_code == 400
    assert group_response.json()['detail'] == f"Gender with name {gender_data['name']} already exists!"
    assert group_response.json()['status'] == 0
    
    
def test_disable_gender(client_instance, get_session, admin_login):
    # Seeding data into database before testing deactivate function
    gender_data = {
        'name': 'male',
        'slug': 'slug',
        'status': True
    } 
    new_gender = GenderModel(**gender_data)
    get_session.add(new_gender)
    get_session.commit()
    
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # deactivate.
    gender_response = client_instance.patch('/gender/disable/slug', headers=headers)
    get_session.commit()
    assert gender_response.status_code == 200
    # check the status of the user group.
    disabled_gender = get_session.query(GenderModel).filter_by(name=gender_data['name']).first()
    assert disabled_gender.status is False
    
def test_enable_gender(client_instance, get_session, admin_login):
    # Seeding data into database before testing deactivate function
    gender_data = {
        'name': 'male',
        'slug': 'slug',
        'status': False
    } 
    new_gender = GenderModel(**gender_data)
    get_session.add(new_gender)
    get_session.commit()
    
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # deactivate.
    gender_response = client_instance.patch('/gender/enable/slug', headers=headers)
    get_session.commit()
    assert gender_response.status_code == 200
    # check the status of the user group.
    disabled_gender = get_session.query(GenderModel).filter_by(name=gender_data['name']).first()
    assert disabled_gender.status is True
    
def test_view_all_genders(client_instance, get_session, admin_login):
    # seed the database for gender
    seed_gender(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # all gender.
    genders = get_session.query(GenderModel).all()
    assert len(genders) > 0
    gender_response = client_instance.get('/gender/', headers=headers)
    assert len(gender_response.json()['data']) == len(genders)
    assert gender_response.status_code == 200
    
def test_view_all_enabled_genders(client_instance, get_session, admin_login):
    # seed the database for gender
    seed_gender(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    # all active gender.
    active_genders = get_session.query(GenderModel).filter_by(status=True).all()
    assert len(active_genders) > 0
    
    gender_response = client_instance.get('/gender/active', headers=headers)
    assert len(gender_response.json()['data']) == len(active_genders)
    assert gender_response.status_code == 200
    
def test_view_single_gender(client_instance, get_session, admin_login):
    # add the data.
    gender_data = {
        'name': 'male',
        'slug': 'slug',
        'status': True
    } 
    new_gender = GenderModel(**gender_data)
    get_session.add(new_gender)
    get_session.commit()
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    gender_response = client_instance.get('/gender/slug', headers=headers)
    assert gender_response.status_code == 200
    assert gender_response.json()['data']['name'] == 'male'   