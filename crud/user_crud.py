import sys
from fastapi import HTTPException
# from sqlalchemy.orm import Session, load_only
sys.path.append("..")
from utils import *
from auth_token import *
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
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from utils import (
    check_password,
    remove_fields,
    model_to_dict
)

db = Session()
hasher = PasswordHasher()
 
# user login
def user_login(db, client_id, username, password):
    try:
        # check if the user exists.
        check_user = models.ClientUsers.check_client_username(db, client_id, username)
        if check_user is None:
            return exceptions.bad_request_error(f"user with username: {username} doesn't exist")
        if not check_user.status:
            return exceptions.bad_request_error("Account is disabled")
        
        if hasher.verify(check_user.password, password):
            get_token = create_token(check_user)
        
    except VerifyMismatchError as e:
        return exceptions.bad_request_error("Incorrect Password")
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
    return success_response.success_message(get_token)

# create new user.
def create_user(db, current_user: models.ClientUsers, new_user):
    try:
        # check if the username exists.
        check_client = models.ClientUsers.check_client_username(db, current_user.client_id, new_user.username_address.lower())
        if check_client is not None:
            return exceptions.bad_request_error(f"user with username {new_user.username.lower()} already exists")
        # create the user
        new_user_dict = new_user.dict(exclude_unset = True)
        new_user_dict['client_id'] = current_user.client_id
        # check the password strength.
        password = new_user_dict['password']
        if not check_password(password):
            return exceptions.bad_request_error("Password did not meet requirement.")
            
        new_user_dict['password'] = hasher.hash(password)
        new_user_dict['username'] = new_user_dict['username'].lower()
        create_new_user = models.ClientUsers.create_client_users(new_user_dict)
        if create_new_user is None:
            return exceptions.bad_request_error("Error occurred while creating user")
        # add and commit
        db.add(create_new_user)
        db.commit()
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
    return success_response.success_message([], "New User was successfully created", 201)

def admin_login(db, client_id, user_username, user_password):
    if client_id != 1:
        return exceptions.unauthorized_error(detail="you don't have the permission to use this page")
    
    return user_login(db, client_id, user_username, user_password)

def refresh_token(db, token):
    bool_result, token_data = verify_refresh_token(db, token)
        
    if not bool_result:
        return exceptions.unauthorized_error(token_data)
    
    return success_response.success_message(token_data)

def get_details(db, current_user):
    try:
        fields_to_remove = ['id', 'admin', 'slug', 'client_key', 'status', 'password', 'updated_at', 'created_at']  # Specify the fields you want to remove
        #filtered_data = remove_fields(current_user.__dict__, fields_to_remove)            
        filtered_data = model_to_dict(current_user.__dict__)
        user_data = remove_fields(filtered_data, fields_to_remove) 
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
    return success_response.success_message(user_data)

def update_details(db, username, current_user, update_data):
    try:
        # convert the data to dict.
        updated_dict = update_data.dict(exclude_unset=True, exclude_none=True)
        # check if the username exists for that client.
        check_user = models.ClientUsers.check_client_username(db, current_user.client_id, username.lower())
        if check_user is None:
            return exceptions.bad_request_error(f"username {username} doesn't exist for client")
        
        if check_user.username == current_user.username:
            return exceptions.bad_request_error(f"you are not allowed to update your account")
        
        # check if you are updating username for the user.
        if updated_dict.get('username') is not None:
            existing_user = models.ClientUsers.check_client_username(db, current_user.client_id, updated_dict['username'])
            if existing_user is not None:
                return exceptions.bad_request_error(f"username {username} already in use.")
        
        # update from here.
        update_user = models.ClientUsers.update_client_user(db, check_user.id, updated_dict)
        if not update_user:
            return exceptions.bad_request_error("An error ocurred while updating User, Please try again")
        db.add(update_user)
        db.commit()
        db.refresh(update_user)
    
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
    return success_response.success_message(update_user, "User record was successfully updated")