import sys
sys.path.append("..")
from utils import *
from db import client_model as models
from db.session import Session
from fastapi_pagination import Params
from response_handler import error_response as exceptions
from response_handler import success_response
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import load_only
from auth_token import *
from uuid import uuid4
from slugify import slugify

db = Session() 

# create unique client slug from client name.
def generate_client_slug(db, client_name):
    counter = 1
    client_id = models.Client.get_client_object(db).count()
    base_slug = slugify(f"{client_name}-{client_id}")
    slug = base_slug
    while models.Client.check_slug(db, slug) is not None:
        counter += 1
        slug = f"{base_slug}{counter}"
        
    return slug

# generate unique client key
def generate_client_key(db):
    client_key = str(uuid4())
    # check if the key exists.
    while models.Client.check_single_key(db, client_key) is not None:
        client_key = str(uuid4())
        
    return client_key
    
    

def create_new_client(db, client_details):
    # first check if the client is already present.
    try:
        # get the slug.
        client_slug = generate_client_slug(db, client_details.client_name)
        # get the client key.
        client_key = generate_client_key(db)
        # convert the client_details to a dictionary.
        client_data = client_details.dict(exclude_unset = True)
        client_data['slug'] = client_slug
        client_data['client_key'] = client_key
        
        create_client = models.Client.create_single_client(client_data)
        if create_client is None:
            return exceptions.bad_request_error("An error ocurred while creating client, Please try again")  
        
        db.add(create_client)
        db.commit()
        
        result = {
            'slug': client_slug,
            'client_key' : client_key
        }
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))  

    return success_response.success_message([result], "Client was successfully created", 201)
    
def update_client(db, client_id, update_client_data):
    try:
        get_client = models.Client.get_client_by_id(db, client_id)
        if get_client is None:
            return exceptions.bad_request_error("Client with such id does not exists")   
        # update client_field
        update_client_field = models.Client.update_single_client(db, client_id, update_client_data.dict(exclude_unset=True))        
        if not update_client_field:
            return exceptions.bad_request_error("An error ocurred while updating client, Please try again")
            
        db.add(update_client_field)
        db.commit()
        db.refresh(update_client_field)
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))  

    return success_response.success_message(update_client_field, "Client record was successfully updated")
    
def update_client_key(db, client_id, new_key):
    try:
        # check if the old key exists;
        get_client = models.Client.check_single_key(db, new_key.client_key)
        if get_client is not None:
            return exceptions.bad_request_error("Client with such key already exists")
                
        return update_client(db, client_id, new_key)
           
    except Exception as e:
        return exceptions.server_error(str(e)) 
    
def get_all_clients(db, page: int, page_size: int):
    try:  
        # get the client object for the desired columns.
        client_object = models.Client.get_client_object(db).options(
            load_only('id'),
            load_only('slug'),
            load_only('status')
        )
        # calculate page offset.
        page_offset = Params(page=page, size=page_size)

        data_result = paginate(client_object, page_offset)
      
        return success_response.success_message(data_result)
        
    except Exception as e:
        return exceptions.server_error(str(e))
    
def change_client(db, client_slug, user_payload):
    try:
        # get the active client (logged in client)
        get_user = get_active_user(db, user_payload)
        # check if the user is actual an admin or not.
        if not get_user.admin:
            return exceptions.bad_request_error("Error, User does not have that privilege")
        # check if the client_slug exists.
        find_client = models.Client.get_client_object(db).filter_by(
            slug=client_slug
        ).first()
        
        if find_client is None:
            return exceptions.bad_request_error(detail=f"Client with slug {client_slug} doesn't exist")
        # regenerate the token.
        new_token = create_token(get_user, selected_client_id = find_client.id)    
        return success_response.success_message(new_token)
            
    except Exception as e:
        return exceptions.server_error(str(e))
    