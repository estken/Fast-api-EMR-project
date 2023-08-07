import sys
# from sqlalchemy.orm import Session, load_only
sys.path.append("..")
from utils import *
from auth_token import *
from db import client_model as models
from db.session import Session
from response_handler import error_response as exceptions
from response_handler import success_response
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from utils import (
    check_password,
    remove_fields,
    model_to_dict
)
import random

db = Session()
hasher = PasswordHasher()

def check_centers(db, center_list, client_id):
    error_message = ""
    check_all = True
    center_list = [center_name.lower() for center_name in center_list]
    
    existing_centers = models.ClientCenter.get_center_object(
        db).filter(models.ClientCenter.slug.in_(center_list)).all()
    
    # Create a dictionary to store center names as keys and IDs as values
    center_name = {center.slug: center.id for center in existing_centers if center.status}
    # check if there are any inactive centers based on the slugs supplied.
    inactive_centers = [center.slug for center in existing_centers if not center.status]
    
    if len(inactive_centers) > 0:
        return False, ["Error: Inactive Centers", inactive_centers], ""
        
    # get the missing centers, that's the supplied centers that are not valid.
    missing_centers = set(center_list) - set(center_name.keys())
    if len(missing_centers) != 0:
        check_all = False
        error_message = ["Error: Centers don't exist:", list(missing_centers)]
    
    return check_all, error_message, list(center_name.values())

def filter_fields(user: models.ClientUsers, fields: list):
    filtered_data = model_to_dict(user.__dict__)
    user_data = remove_fields(filtered_data, fields) 
    return user_data

"""
check if the user is required to reset the password or probably change their password to something
"""
def check_password_stat(user: models.ClientUsers):
    if user.is_reset:
        return False, [{"is_reset": True}]
    
    return True, ""

def set_lock(db, user: models.ClientUsers, logged_in = False):
    is_locked = False
    if user.invalid_password > 5:
        is_locked = True
        
    if logged_in:
        password_count = 0
    else:
        password_count = user.invalid_password + 1
        
    update_user_lock = {
        "invalid_password": password_count,
        "is_locked": is_locked
    }
    update_user = models.ClientUsers.update_client_user(db, user.id, update_user_lock)
    db.add(update_user)
    db.commit()
    db.refresh(update_user)
    
# user login
def user_login(db, client_id, username, password):
    try:
        # check if the user exists.
        check_user = models.ClientUsers.check_client_username(db, client_id, username)
        if check_user is None:
            return exceptions.bad_request_error("username or password  is incorrect")
        
        
        if hasher.verify(check_user.password, password):
            # check if the user's account is active or not.
            if not check_user.status:
                return exceptions.bad_request_error("Account is disabled")
            # checked if password is locked here.
            if check_user.is_locked:
                return exceptions.forbidden_error(detail="Sorry, user's account is locked")
            # reset password lock on successful login.
            set_lock(db, check_user, logged_in = True)
            get_token = create_token(check_user)
            
            return success_response.success_message(get_token)

    except VerifyMismatchError as e:
        # increase number.
        set_lock(db, check_user)
        return exceptions.bad_request_error("Incorrect Username or Password")
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
# create new user.
def create_user(db, user_payload, new_user):
    try:
            # get the current_user from the user payload.
        selected_client_id = user_payload.get("selected_client_id")
        current_user = get_active_user(db, user_payload)
        # check if the username exist.
        check_client = models.ClientUsers.check_client_username(db, selected_client_id, new_user.username.lower())
        if check_client is not None:
            return exceptions.bad_request_error(f"user with username {new_user.username.lower()} already exists")
        # check if the center(s) exists.
        bool_result, err_mess, center_ids = check_centers(db, new_user.center, selected_client_id)
        if not bool_result:
            return exceptions.bad_request_error(err_mess[0], err_mess[1])
                
        # create the user
        new_user_dict = new_user.dict(exclude_unset = True)
        new_user_dict['client_id'] = selected_client_id
        # check the password strength.
        password = new_user_dict['password']
        bool_result, message = check_password(password, new_user_dict['username'])
        if not bool_result:
            return exceptions.bad_request_error(message)
            
        new_user_dict['password'] = hasher.hash(password)
        new_user_dict['username'] = new_user_dict['username'].lower()
        # remove center from the dictionary since it's not a valid field in the model.
        new_user_dict.pop('center')
        create_new_user = models.ClientUsers.create_client_users(new_user_dict)
        if create_new_user is None:
            db.rollback()
            return exceptions.bad_request_error("Error occurred while creating user")
        # add and commit
        db.add(create_new_user)
        
        #create the user and center.
        user_center = models.UserCenter.bulk_create(center_ids, create_new_user.id,
                                                    random.choice(center_ids))
        if not user_center:
            db.rollback()
            return exceptions.bad_request_error("An error occurred when trying to map user to centers, please try again.") 
        
        db.add_all(user_center)
        db.commit()
        
        return success_response.success_message([], "New User was successfully created", 201)

    except Exception as e:
        db.rollback()
        return exceptions.server_error(detail=str(e))
    

def admin_login(db, client_id, user_username, user_password):
    if client_id != 1:
        return exceptions.unauthorized_error(detail="you don't have the permission to use this page")
    
    return user_login(db, client_id, user_username, user_password)

def refresh_token(db, token):
    bool_result, token_data = verify_refresh_token(db, token)
        
    if not bool_result:
        return exceptions.unauthorized_error(token_data)
    
    return success_response.success_message(token_data)

def get_details(db, user_payload):
    try:
        fields_to_remove = ['id', 'admin', 'slug', 'client_key', 
                            'status', 'password', 'updated_at', 
                            'created_at', 'is_reset', 'invalid_password',
                            'is_locked', 'client']  # Specify the fields you want to remove
        
        current_user = get_active_user(db, user_payload)
        user_data = filter_fields(current_user, fields_to_remove)
        
        return success_response.success_message(user_data)

    except Exception as e:
        return exceptions.server_error(detail=str(e))
    

def update_details(db, username, user_payload, update_data):
    try:
        # convert the data to dict.
        updated_user_dict = update_data.dict(exclude_unset=True, exclude_none=True)
        # get the current_user from the user payload.
        current_user = get_active_user(db, user_payload)
        # check if the username exists for that client.
        check_user = models.ClientUsers.check_client_username(db, current_user.client_id, username.lower())
        if check_user is None:
            return exceptions.bad_request_error(f"username {username} doesn't exist for client")
        
        if check_user.username == current_user.username:
            return exceptions.bad_request_error(f"you are not allowed to update your account")
        
        # check if you are updating username for the user.
        if updated_user_dict.get('username') is not None:
            existing_user = models.ClientUsers.check_client_username(db, current_user.client_id, updated_user_dict['username'])
            if existing_user is not None:
                return exceptions.bad_request_error(f"username {updated_user_dict['username']} already in use.")        
        # update from here.
        update_user = models.ClientUsers.update_client_user(db, check_user.id, updated_user_dict)
        if not update_user:
            return exceptions.bad_request_error("An error ocurred while updating User, Please try again")
        db.add(update_user)
        db.commit()
        db.refresh(update_user)
        
        fields_to_remove = ['id', 'admin', 'slug', 'client_key', 
                            'status', 'password', 'updated_at', 
                            'created_at', 'invalid_password',
                            'client']  # Specify the fields you want to remove
        user_data = filter_fields(update_user, fields_to_remove)
        
        return success_response.success_message(user_data, "User record was successfully updated")
    
    except Exception as e:
        return exceptions.server_error(detail=str(e))