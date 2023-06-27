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
from utils import check_password

db = Session()
hasher = PasswordHasher()
 
# user login
def user_login(db, client_id, email, password):
    try:
        # check if the user exists.
        check_user = models.ClientUsers.check_client_email(db, client_id, email)
        if check_user is None:
            return exceptions.bad_request_error(f"user with email address: {email} doesn't exist")
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
        # check if the email exists.
        check_client = models.ClientUsers.check_client_email(db, current_user.client_id, new_user.email_address.lower())
        if check_client is not None:
            return exceptions.bad_request_error(f"user with email address {new_user.email_address.lower()} already exists")
        # create the user
        new_user_dict = new_user.dict(exclude_unset = True)
        new_user_dict['client_id'] = current_user.client_id
        # check the password strength.
        password = new_user_dict['password']
        if not check_password(password):
            return exceptions.bad_request_error("Password did not meet requirement.")
            
        new_user_dict['password'] = hasher.hash(password)
        create_new_user = models.ClientUsers.create_client_users(new_user_dict)
        if create_new_user is None:
            return exceptions.bad_request_error("Error occurred while creating user")
        # add and commit
        db.add(create_new_user)
        db.commit()
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
    return success_response.success_message([], "New User was successfully created", 201)

def admin_login(db, client_id, user_email, user_password):
    if client_id != 1:
        return exceptions.unauthorized_error(detail="you don't have the permission to use this page")
    
    return user_login(db, client_id, user_email, user_password)

def refresh_token(db, token):
    try:
        new_token = verify_refresh_token(db, token)
    
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
    return success_response.success_message(new_token)