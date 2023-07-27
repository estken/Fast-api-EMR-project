import sys

from fastapi import HTTPException
# from sqlalchemy.orm import Session, load_only

sys.path.append("..")
from utils import *
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
from slugify import slugify

db = Session()

def generate_slug(db, user, center_name):
    counter = 1
    client_id = user.client_id
    base_slug = slugify(f"{center_name}-{client_id}")
    slug = base_slug
    while models.ClientCenter.check_slug(db, slug) is not None:
        counter += 1
        slug = f"{base_slug}{counter}"
        
    return slug

def create_center(db, user_payload, center_detail):
    try:
        # get the active logged in user and the selected whose center is to created.
        get_user = get_active_user(db, user_payload)
        selected_client_id = user_payload.get("selected_client_id") 
        # convert the center_detail to dictionary
        center_data = center_detail.dict(exclude_unset = True)
        center_data['slug'] = generate_slug(db, get_user, center_detail.center)
        # create the center for the client.
        created_center = models.ClientCenter.create_center(
            center_data
        )
        if created_center is None:
            return exceptions.bad_request_error("An error occurred while creating center for client")
        db.add(created_center)
        db.commit()
        
        return success_response.success_message([], f"Center {center_data['center']} was successful created", 201)
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
def update_center(db, user_payload, update_center_data, center_slug):
    try:
        # first check if the center id exists or not.
        check_center = models.ClientCenter.check_slug(db, center_slug)
        if check_center is None:
            return exceptions.bad_request_error("Sorry Center does not exists")
        # get the center id.
        center_id = check_center.id
        # update right away.
        update_center = models.ClientCenter.update_center(db, center_id, update_center_data)
        
        if update_center is None:
            return exceptions.bad_request_error("An error occurred while updating data")
        db.add(update_center)
        db.commit()
        db.refresh(update_center)
        
        return success_response.success_message(update_center, "Center was successfully updated")
    
    except Exception as e:
        return exceptions.server_error(detail=str(e))

def update_center_status(db, user_payload, center_slug, state):
    """This function updates a centers status"""
    try:
        # first check if the center id exists or not.
        check_center = models.ClientCenter.check_slug(db, center_slug.slug)
        if check_center is None:
            return exceptions.bad_request_error("Sorry Center does not exists")
            
        if state == check_center.status:
            if state:
                return exceptions.bad_request_error("Center is already Enabled")
            return exceptions.bad_request_error("Center is already Disabled")
        # get the center id.
        center_id = check_center.id
        # update right away.
        update_center = models.ClientCenter.update_center(db, center_id, {'status': state})
        
        if update_center is None:
            return exceptions.bad_request_error("An error occurred while updating data")
        db.add(update_center)
        db.commit()
        db.refresh(update_center)
        
        return success_response.success_message(update_center, "update was carried out successfully")
        
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))

def get_center(db, user_payload, center_slug):
    try:
        # check if slug exists.
        check_center = models.ClientCenter.check_slug(db, center_slug)
        if check_center is None:
            return exceptions.bad_request_error("Sorry Center does not exists")
        
        return success_response.success_message(check_center)
    
    except Exception as e:
        return exceptions.server_error(detail=str(e))
        
def get_centers(db, user_payload):
    try:
        # get the user payload for the centers.
        selected_client_id = user_payload.get("selected_client_id")
        centers = models.ClientCenter.get_all_center(db)
        
        return success_response.success_message(centers)
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))