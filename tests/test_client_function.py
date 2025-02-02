from .conftest import get_session, client_instance
import sys
sys.path.append("..")
from db import client_model as models
from schema import ClientSchema, UpdateStatusSchema, UpdateClientKeySchema
import uuid
from fastapi import status
# from fastapi.testclient import TestClient
# from apis.client import client_router
# from main import notification_app
from .seeder import (
    seed_client
)
import logging

# Add this line to configure logging
logging.basicConfig(level=logging.DEBUG)

# return client with slug name.
def look_up_client(db, slug_name):
    return db.query(models.Client).filter(models.Client.slug == slug_name).first()

def test_ping(client_instance):
    # check root URL
    root_response = client_instance.get("/")
    assert root_response.status_code == 200
    assert root_response.json()['detail'] == "Access Control Application is up"

def test_create_client(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'client_name': 'testing'
    }
    # check the length of the table before insertion
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 0
    # get the client router
    client_response = client_instance.post("/client/create", json=client_data)
    
    assert client_response.status_code == 201
    assert client_response.json()['detail'] == "Client was successfully created"
    assert client_response.json()['status'] == 1
    #check the length of the table to be sure it has increased.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    # check if the vaues of attributes created.
    get_details = models.Client.get_client_by_id(get_session, 1)
    assert get_details.slug is not None
    assert get_details.client_key is not None
    assert get_details.status == True

def test_create_client_insert_error(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'slug': None,
        'client_key': str(uuid.uuid4())
    }
    
    # unprocessiable entity error.
    client_response = client_instance.post("/client/create", json=client_data)
    
    assert client_response.status_code != 201
    

def test_deactivate_client_with_middleware(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'client_name': 'testing',
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    created_client = models.Client(**client_data)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    # header.
    headers = {
        "Client-Authorization": client_data['client_key']
    }
    # update the client status.
    client_response = client_instance.patch("/client/deactivate", headers=headers)
    # force commit after updating.
    get_session.commit()
    assert client_response.status_code == 200
    assert client_response.json()['status'] == 1
    
    # check if it was successfully updated.
    updated_data = look_up_client(get_session, client_data['slug'])
    assert updated_data is not None
    assert updated_data.slug == client_data['slug']
    assert updated_data.status == False
    

def test_deactivate_client_without_middleware(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'client_name': 'testing',
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    created_client = models.Client(**client_data)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    # update the client status without headers
    client_response = client_instance.patch("/client/deactivate")
    
    assert client_response.status_code == 401
    assert client_response.json()['detail'] == "Client key is missing"
 
def test_deactivate_client_with_deactivated_user(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'client_name': 'testing',
        'slug': 'client-A',
        'client_key': str(uuid.uuid4()),
        'status': False
    }
    
    created_client = models.Client(**client_data)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    
    # header.
    headers = {
        "Client-Authorization": client_data['client_key']
    }
    # update the client status with headers
    client_response = client_instance.patch("/client/deactivate", headers=headers)
    
    assert client_response.status_code == 401
    assert client_response.json()['detail'] == "Inactive account"
 
                    
def test_update_client_key_with_middleware(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'client_name': 'testing',
        'slug': 'client-A',
        'client_key': "old client key"
    }

    created_client = models.Client(**client_data)
    get_session.add(created_client)
    get_session.commit()
    
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    
    # header.
    headers = {
        "Client-Authorization": client_data['client_key']
    }
    # update the key. 
    new_key = {
        'client_key':"new key"
    }
    
    new_key_data = UpdateClientKeySchema(**new_key)
    client_response = client_instance.patch("/client/update", json=new_key, headers=headers)
    # force commit to ensure update happens immediately.
    get_session.commit()
    assert client_response.status_code == 200
    # check if the key has been updated
    updated_data = look_up_client(get_session, client_data['slug'])
    assert updated_data is not None
    # check if it doesn't have the key stored as old key anymore.
    # client.client_key = "Old key"
    assert updated_data.client_key != client_data['client_key']
    # check if it was updated correctly.
    assert updated_data.slug == client_data['slug']
    assert updated_data.status == True
    assert updated_data.client_key == "new key"
    
def test_update_client_key_with_deactivated_user(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'client_name': 'testing',
        'slug': 'client-A',
        'client_key': str(uuid.uuid4()),
        'status': False
    }
    
    created_client = models.Client(**client_data)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # ensure it was created.
    retrieve_clients = models.Client.retrieve_all_client(get_session)
    assert len(retrieve_clients) == 1
    
    # header.
    headers = {
        "Client-Authorization": client_data['client_key']
    }
    # update the key. 
    new_key = {
        'client_key':"new key"
    }
    # update the client status with headers
    client_response = client_instance.patch("/client/update", json=new_key, headers=headers)
    
    assert client_response.status_code == 401
    assert client_response.json()['detail'] == "Inactive account"


def test_reactivate_client(client_instance, get_session):
    # data to populate the table with.
    client_data = {
        'client_name': 'testing',     
        'slug': 'client-A',
        'client_key': str(uuid.uuid4()),
        'status': False
    }
    
    created_client = models.Client(**client_data)
    get_session.add(created_client)
    get_session.commit()
    
    assert created_client is not None
    # check if the client is False.
    assert created_client.status == False
    # ensure it was created.
    client_response = client_instance.patch(f"/client/reactivate/1")
    get_session.commit()
    assert client_response.status_code == 200
    assert client_response.json()['status'] == 1
    # check if the key has been updated
    updated_data = look_up_client(get_session, client_data['slug'])
    assert updated_data is not None
    assert updated_data.status == True
            
def test_get_all_clients(client_instance, get_session):
    seed_client(get_session)
    
    # page 1 with 1 rcords per page
    client_response = client_instance.get("/client/", params={"page":1, "page_size":1})
    assert len(client_response.json()['data']['items'])== 1
    assert client_response.status_code == 200
    
def test_get_all_clients_with_error(client_instance, get_session):
    # happens when we are accessing a page less than 0.
    client_data = {
        'client_name': 'testing',
        'slug': 'client-A',
        'client_key': str(uuid.uuid4())
    }
    
    created_client = models.Client(**client_data)
    get_session.add(created_client)
    get_session.commit()
    
    client_data = {
        'client_name': 'testing2',
        'slug': 'client-B',
        'client_key': str(uuid.uuid4())
    }
    
    created_client = models.Client(**client_data)
    get_session.add(created_client)
    get_session.commit()
    # page 1 with 1 rcords per page
    client_response = client_instance.get("/client/", params={"page":0, "page_size":1, "page_number": 0})
    assert client_response.status_code == 422

    
def test_get_all_clients_without_size(client_instance, get_session):
    seed_client(get_session)
    # first check the length without pagination.
    get_clients = models.Client.retrieve_all_client(get_session)
    assert len(get_clients) == 12
    # call the paginated endpoint, default size is 10.
    # default page is 1.
    client_response = client_instance.get("/client/")
    assert len(client_response.json()['data']['items'])== 10
    assert client_response.status_code == 200
    assert client_response.json()['data']['page'] == 1