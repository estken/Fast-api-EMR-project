import sys

from fastapi import HTTPException
# from sqlalchemy.orm import Session, load_only

sys.path.append("..")
from utils import *
from typing import List
from db import models
from db.session import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_pagination import Page, Params
from response_handler import error_response as exceptions
from response_handler import success_response
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import load_only, joinedload, selectinload
from sqlalchemy import and_
from datetime import datetime

db = Session()

def check_group_slug(db, client_id, user_data):
    get_slug = models.UserGroup.user_group_object(db).filter_by(
            client_id=client_id, slug= user_data.slug).first()
    get_name = models.UserGroup.user_group_object(db).filter_by(
        client_id=client_id, group_name= user_data.group_name).first()
    
    if get_slug is not None:
        return False, f"Sorry, User Group with slug name {user_data.slug} exists for this client"
    if get_name is not None:
        return False, f"Sorry, User Group with group name {user_data.group_name} exists for this client"
    
    return True, ""

def check_client_id(db, user_group_id, client_id):
    # first check if the user_id exists for that client.
    get_user_id = models.UserGroup.get_user_group_by_id(db, user_group_id)
    if get_user_id is None:
        return False, "No User Group with such ID"
    
    if get_user_id.client_id != client_id:
        return False, "Group ID doesn't belong to client"
    
    return True, ""


def create_user_group(db, client_id, user_data, route_name):
    # first check if the client is already present.
    try:
        # check if the slug and group name exists for the client.
        bool_result, message = check_group_slug(db, client_id, user_data)
        if not bool_result:
            return exceptions.bad_request_error(message)
        # convert this to a dictionary
        user_dict = user_data.dict(exclude_unset=True)
        user_dict['client_id'] = client_id
        # create the user group
        create_user_group = models.UserGroup.create_user_group(user_dict)       
        if create_user_group is None:
            return exceptions.bad_request_error("An error ocurred while creating UserGroup, Please try again")  
        
        db.add(create_user_group)
        db.commit()
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))  

    return success_response.success_message([], "UserGroup was successfully created", 201)

def update_group(db, client_id, user_group_id, update_data, route_name):
    try:
        # first check if the user_id exists for that client.
        bool_result, message = check_client_id(db, user_group_id, client_id)
        if not bool_result: 
            return exceptions.bad_request_error(message)
        # update right away.
        updated_group = models.UserGroup.update_user_group(db, user_group_id, update_data)
        if not updated_group:
            return exceptions.bad_request_error("An error occurred while updating user group")
        # update.
        db.add(updated_group)
        db.commit()
        db.refresh(updated_group)   
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
    return success_response.success_message(updated_group, "User Group was successfully updated")

def update_group_data(db, client_id, user_group_id, update_data, route_name):
    """Update data of an existing client group"""
    # check if the slug and group name exists for the client.
    bool_result, message = check_group_slug(db, client_id, update_data)
    if not bool_result:
        return exceptions.bad_request_error(message)
    
    user_dict = update_data.dict(exclude_unset=True)

    return update_group(db, client_id, user_group_id, user_dict, route_name)

def get_groups(db, client_id, page, page_size, route_name):
    try:
        client_group = models.UserGroup.get_client_user_groups(db, client_id).options(
            load_only('id'),
            load_only('slug'),
            load_only('group_name'),
            load_only('status')
        )
        
        #calculate the offset.
        page_offset = Params(page=page, size=page_size)
        data_result = paginate(client_group, page_offset)
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
    return success_response.success_message(data_result)

def single_group(db, client_id, group_id, route_name):
    try:
        # first check if the user_id exists for that client.
        bool_result, message = check_client_id(db, group_id, client_id)
        if not bool_result: 
            return exceptions.bad_request_error(message)
        
        data_result = models.UserGroup.user_group_object(db).options(
            load_only('slug'),
            load_only('group_name'),
            load_only('status')  
        ).get(group_id)
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
    return success_response.success_message(data_result)
