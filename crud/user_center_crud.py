import sys
from fastapi import HTTPException
# from sqlalchemy.orm import Session, load_only
sys.path.append("..")
from utils import *
from auth_token import *
from typing import List
from db import client_model as models
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
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from utils import (
    check_password,
    remove_fields,
    model_to_dict
)
from crud import user_crud

def check_uuid(db, client_id, user_uuid):
    get_client = models.ClientUsers.check_client_username(
            db, client_id, user_uuid)
    
    if get_client is None:
        return False, "user with such uuid doesnot exist"
    
    return True, get_client 

def check_user_center(db, center_details, user_payload):
    """ check if the user already has those center(s) added to their database """
    selected_client_id = user_payload.get("selected_client_id")
        # check if the uuid exists.
    username = center_details.username
    # check if username or uuid exists and return the id.
    bool_result, data = check_uuid(db, selected_client_id, username)
    if not bool_result:
        return False, "User with such username doesn't exist", ""
    # check if the center(s) exists.
    bool_result, err_mess, center_ids = user_crud.check_centers(
        db, center_details.center, selected_client_id)
    # check if the return result is false.
    if not bool_result:
        return False, err_mess, ""
    
    return True, data, center_ids


def set_new_default(db, user_id):
    # check for default center.abs
    get_default = models.UserCenter.user_center_object(
        db).filter(models.UserCenter.user_id == user_id,
                   models.UserCenter.is_default == True).first()
    
    # if no default is set yet.
    if get_default is None:
        default_data = {
            "is_default": True
        }
        # get user center.
        get_user_center = models.UserCenter.user_center_object(
            db).filter(models.UserCenter.user_id == user_id).first()
        # update the data.
        update_default = models.UserCenter.update_user_center(
            db,get_user_center.id, default_data)
        db.add(update_default)
        db.commit()
        db.refresh(update_default)
        
def existing_user_center(db, existing_centers, center_ids):
    # check all the ids not present.
    if len(existing_centers) != len(center_ids):
        existing_id = [center.center_id for center in existing_centers]
        # get the set difference.
        center_diff = set(center_ids) - set(existing_id)
        slug_diff = models.ClientCenter.get_center_object(
            db).filter(models.ClientCenter.id.in_(center_diff)).all()
        
        err_message = [center.slug for center in slug_diff] 
        return False, "The following centers don't exist for user: " + ", ".join(err_message)
    
    return True, ""
       
       
def get_user_centers(db, user_uuid, user_payload):
    try:
        # get the selected client id.
        selected_client_id = user_payload.get('selected_client_id')
        # get the username.
        username = user_uuid.username
        # check if username or uuid exists and return the id.
        bool_result, data = check_uuid(db, selected_client_id, username)
        if not bool_result:
            return exceptions.bad_request_error("User with such username doesn't exist")
        # get the centers attached to the centers.
        all_centers = models.UserCenter.user_center_object(db).options(
            joinedload(models.UserCenter.client_centers).load_only('slug').options(
                load_only('slug'),
                load_only('center')),
            load_only('id')
        )
        all_centers = all_centers.filter(
            models.UserCenter.user_id == data.id).all()
        
        return success_response.success_message(all_centers)
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))

def check_existing_center(db, existing_centers):
    if len(existing_centers) != 0:
        # convert to a list
        center_list = [center.center_id for center in existing_centers]
        # check the model list to get all the records
        existing_slugs = models.ClientCenter.get_center_object(
            db).filter(models.ClientCenter.id.in_(center_list))
        # get the existing slugs
        slug_list = [center.slug for center in existing_slugs]
        message = "The following centers already exists for user: " + ", ".join(slug_list)
        
        return False, message
    
    return True, ""     
    
def add_new_center(db, center_details, user_payload):         
    try:
        # check user, centers and other properties.
        bool_result, data, center_ids = check_user_center(
            db, center_details, user_payload)
        
        if not bool_result:
            return exceptions.bad_request_error(data)
        
        existing_centers = models.UserCenter.user_center_object(
            db).filter(models.UserCenter.user_id == data.id,
                       models.UserCenter.center_id.in_(center_ids)).all()
    
        bool_result, message = check_existing_center(db, existing_centers)
        if not bool_result:
            return exceptions.bad_request_error(message)
    
        
        create_center = models.UserCenter.bulk_create(center_ids, data.id, -1)
        if not create_center:
            db.rollback()
            return exceptions.bad_request_error("An error occurred when trying to map user to centers, please try again.") 
        
        db.add_all(create_center)
        db.commit()
        
        return success_response.success_message([], "Center was successfully added for user")
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))
         
def remove_center(db, center_details, user_payload):
    try:
        # check user, centers and other properties.
        bool_result, data, center_ids = check_user_center(
            db, center_details, user_payload)
        
        if not bool_result:
            return exceptions.bad_request_error(data)
        
        existing_centers = models.UserCenter.user_center_object(
            db).filter(models.UserCenter.user_id == data.id,
                       models.UserCenter.center_id.in_(center_ids)).all()
    
        bool_result, message = existing_user_center(db, existing_centers, 
                                                    center_ids)
        if not bool_result:
            return exceptions.bad_request_error(message)     
        # check if the existing centers is equal to number of centers for the user.
        user_centers = models.UserCenter.get_user_centers(
            db, data.id)
        if len(user_centers) == len(existing_centers):
            return exceptions.bad_request_error("User must have atleast 1 center")
        # remove the center ids immediately.
        removed_centers = models.UserCenter.user_center_object(
            db).filter(models.UserCenter.user_id == data.id,
                       models.UserCenter.center_id.in_(center_ids)).delete()
        db.commit()
        # check if there is no default center and make it default.
        set_new_default(db, data.id)
        
        return success_response.success_message([], "Center was successfully deleted for user")
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
def set_default_center(db, user_center, user_payload):
    try:
        selected_client_id = user_payload.get("selected_client_id")
            # check if the uuid exists.
        username = user_center.username
        # check if username or uuid exists and return the id.
        bool_result, data = check_uuid(db, selected_client_id, username)
        if not bool_result:
            return False, "User with such username doesn't exist", ""
        # check if slug is present.
        check_slug = models.ClientCenter.check_slug(db, user_center.center)
        if check_slug is None:
            return exceptions.bad_request_error(f"No Center with such slug {user_center.center}")
        
        # check if center is present for the user
        check_user = models.UserCenter.user_center_object(
            db).filter_by(user_id = data.id, center_id = check_slug.id).first()
        # check if the slug exists at first.
        if check_user is None:
            return exceptions.bad_request_error(f"No Center with such slug {user_center.center} for user")
        
        if check_user.is_default:
            return exceptions.bad_request_error("The center has already been set as default")
        
        # unset all centers a False.
        disable_all = models.UserCenter.user_center_object(
            db).filter_by(user_id=data.id).update({"is_default":False})
        # set new default center.
        check_user.is_default = True
        db.add(check_user)
        db.commit()
         
        return success_response.success_message([], "Center was successfully set as default")
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    