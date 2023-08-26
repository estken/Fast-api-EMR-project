import sys
sys.path.append("..")
from utils import *
from db import client_model as models
from db.session import Session
from fastapi_pagination import Params
from response_handler import error_response as exceptions
from response_handler import success_response
from fastapi_pagination.ext.sqlalchemy import paginate
from slugify import slugify

from sqlalchemy.orm import load_only

db = Session()

def generate_slug(db, group_slug):
    counter = 1
    base_slug = slugify(f"{group_slug}")
    slug = base_slug
    while models.UserGroup.check_slug(db, slug) is not None:
        counter += 1
        slug = f"{base_slug}{counter}"
        
    return slug

def check_group_name(db, user_data):
    get_name = models.UserGroup.user_group_object(db).filter_by(
        group_name= user_data.group_name.lower()).first()
    
    if get_name is not None:
        return False, f"Sorry, User Group with group name {user_data.group_name} exists for this client"
    
    return True, ""

def check_group_id(db, user_group_id):
    # first check if the user_id exists for that client.
    get_user_id = models.UserGroup.get_user_group_by_id(db, user_group_id)
    if get_user_id is None:
        return False, "No User Group with such ID"
    
    return True, ""


def create_user_group(db, user_data):
    # first check if the client is already present.
    try:
        # check if the slug and group name exists for the client.
        bool_result, message = check_group_name(db, user_data)
        if not bool_result:
            return exceptions.bad_request_error(message)
        # convert this to a dictionary
        group_slug = generate_slug(db, user_data.group_name.lower())
        user_dict = user_data.dict(exclude_unset=True)
        user_dict['slug'] = group_slug
        # create the user group
        create_user_group = models.UserGroup.create_user_group(user_dict)       
        if create_user_group is None:
            return exceptions.bad_request_error("An error ocurred while creating UserGroup, Please try again")  
        
        db.add(create_user_group)
        db.commit()
        
        return success_response.success_message([], "UserGroup was successfully created", 201)
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))  

def update_group(db, user_slug, update_data):
    try:
        # first check if the user_slug exists for that client.
        get_slug = models.UserGroup.user_group_object(db).filter_by(
            slug= user_slug.lower()).first()
        if get_slug is None:
            return exceptions.bad_request_error(
                f'No User Group found with Slug Name :{user_slug}')
    
        # update right away.
        updated_group = models.UserGroup.update_user_group(db, get_slug.id, update_data)
        if not updated_group:
            return exceptions.bad_request_error("An error occurred while updating user group")
        # update.
        db.add(updated_group)
        db.commit()
        db.refresh(updated_group)
        
        return success_response.success_message(updated_group, "User Group was successfully updated")

    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
def update_group_data(db, group_slug, update_data):
    """Update data of an existing client group"""
    # check if the slug and group name exists for the client.
    bool_result, message = check_group_name(db, update_data)
    if not bool_result:
        return exceptions.bad_request_error(message)
    
    user_dict = update_data.dict(exclude_unset=True)

    return update_group(db, group_slug, user_dict)

def get_groups(db, page, page_size):
    try:
        client_group = models.UserGroup.get_user_groups(db).options(
            load_only('id'),
            load_only('slug'),
            load_only('group_name'),
            load_only('status')
        )
        
        #calculate the offset.
        page_offset = Params(page=page, size=page_size)
        data_result = paginate(client_group, page_offset)
        
        return success_response.success_message(data_result)

    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
def get_enabled(db):
    try:
        client_group = models.UserGroup.user_group_object(db).options(
            load_only('id'),
            load_only('slug'),
            load_only('group_name'),
            load_only('status')
        ).filter_by(status=True).all()
            
        return success_response.success_message(client_group)
    
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
def single_group(db, group_slug):
    try:
        # first check if the user_id exists for that client.
        get_slug = models.UserGroup.user_group_object(db).filter_by(
            slug= group_slug.lower()).first()
        if get_slug is None:
            return exceptions.bad_request_error(
                f'No User Group found with Slug Name :{group_slug}')
    
        data_result = models.UserGroup.user_group_object(db).options(
            load_only('slug'),
            load_only('group_name'),
            load_only('status')  
        ).get(get_slug.id)
        
        return success_response.success_message(data_result)

    except Exception as e:
        return exceptions.server_error(detail=str(e))
