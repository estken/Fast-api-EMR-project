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

db = Session()

def check_permit(db, router_name):
    # check if the router name exists.
    get_permit = models.Permissions.get_permission_by_name(db, router_name)
    if get_permit is not None:
        return False, f"Permission with name: {router_name} exists", get_permit
    
    return True, "", ""


def create_permission(db, permit_data):
    # first check if the client is already present.
    try:
        # check if the router name already exists.
        bool_result, message, _ = check_permit(db, permit_data.router_name)
        
        if not bool_result:
            return exceptions.bad_request_error(message)
        # convert to a dictionary.
        permit_dict = permit_data.dict(exclude_unset=True)
        # create the permission.
        create_permit = models.Permissions.create_permission(permit_dict)       
        if create_permit is None:
            return exceptions.bad_request_error("An error ocurred while creating new Permission, Please try again")  
        db.add(create_permit)
        db.commit()
        
        return success_response.success_message([], "Permission was successfully created", 201)         
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    

def update_permit(db, router_name, update_permit_data):
    try:
        # first check if the permission exists or not.
        bool_result, _, data = check_permit(db, router_name)
        # if the router doesn't exists.
        if bool_result:
            return exceptions.bad_request_error(f"Permission with name {router_name}")
       
        # check if the status is also being updated.
        get_status = update_permit_data.get('status', None)
        if get_status is not None:
            # check if the status already has that state.
            if get_status == data.status:
                if get_status is True:
                    return exceptions.bad_request_error("Permission is already active")
                return exceptions.bad_request_error("Permission is already disabled")

        
        update_client_permission = models.Permissions.update_permission(
            db, data.id, update_permit_data)
        
                           
        if not update_client_permission:
            return exceptions.bad_request_error("An error ocurred while updating Permission, Please try again")
        db.add(update_client_permission)
        db.commit()
        db.refresh(update_client_permission)
        
        return success_response.success_message(update_client_permission, "User record was successfully updated")

    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
def get_permissions(db, page: int, page_size: int, permit_state = None):
    try:
        data_result = models.Permissions.permission_object(db).options(
            load_only('id'),
            load_only('status'),
            load_only('router_name'),
            load_only('description')
        )
        if permit_state is not None:
            data_result = data_result.filter_by(status=permit_state)
        # calculate page offset.
        page_offset = Params(page=page, size=page_size)

        all_permission = paginate(data_result, page_offset)
      
        return success_response.success_message(all_permission)
            
    except Exception as e:
        return exceptions.server_error(detail=str(e))