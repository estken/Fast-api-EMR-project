from .conftest import get_session, client_instance, admin_login
import sys
sys.path.append("..")
from db.client_model import GenderModel
from schemas.gender_schema import GenderSchema, GenderUpdateSchema
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
    # seed usergroup
    seed_gender(get_session)
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
        'slug': 'slug'
    } 
    new_gender = GenderModel(**gender_data)
    get_session.add(new_gender)
    get_session.commit()
    
    added_gender = get_session.query(GenderModel).filter_by(name=gender_data['name']).first()
    assert added_gender.status is True
    
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
    
    added_gender = get_session.query(GenderModel).filter_by(name=gender_data['name']).first()
    assert added_gender.status is False
    
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
    gender_response = client_instance.get('/gender/active', headers=headers)
    assert len(gender_response.json()['data']) == len(active_genders)
    assert gender_response.status_code == 200
    
def test_view_single_gender(client_instance, get_session, admin_login):
    # seed the database for genders
    seed_gender(get_session)
    # header.
    headers = {
        "Authorization":f"Bearer {admin_login['access_token']}"
    }
    gender_response = client_instance.get('/gender/slug', headers=headers)
    assert gender_response.status_code == 200
    assert gender_response.json()['data']['name'] == 'male'   