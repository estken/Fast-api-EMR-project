import sys
sys.path.append("..")
from utils import *
from db import client_model as models
from db.session import Session
from response_handler import error_response as exceptions
from response_handler import success_response

from sqlalchemy.orm import load_only, joinedload

db = Session()

def check_user_group(db, group_slug):
    
    check_group = models.UserGroup.user_group_object(
            db).filter_by(slug=group_slug).first()
        # check if the group is none or not.
    if check_group is None:
        return False, f"User Group with name: {group_slug} does not exist"
    
    return True, check_group

def check_group_permission(db, router_name):
    # list of permissions
    permission_list = [get_router_name.lower() for get_router_name in router_name]
    # check if the permission really exists.
    valid_permit = models.Permissions.permission_object(
        db).filter(models.Permissions.router_name.in_(permission_list)).all()
    # create a dictionary to store the router and the ids.
    permit_name = {router.id: router.router_name for router in valid_permit}
    missing_permit = set(router_name) - set(permit_name.values())
    
    if len(missing_permit) != 0:
        return False, ["Permission don't exist", list(missing_permit)],  ""
    
    return True, "", permit_name
    
def check_permit_diff(db, existing_permit, required_permit):
    # existing permit relates to permissions already existing for usergroup.
    # required permit relates to permission required to be deleted.
    if len(existing_permit) - len(required_permit.keys())!= 0:
        existing_list = [permit.id for permit in existing_permit]
        missing = set(required_permit.keys()) - set(existing_list)
        missing_list = list(missing)
        missing_router = [required_permit[id] for id in missing_list]
        return False, ["Error: Missing Permissions", missing_router]
    
    return True, ""


def create_user_permit(db, user_permit):
    try:
        # check if the router name already exists for client.
        check_router = models.Permissions.permission_object(
            db).filter_by(router_name=user_permit.router_name).first()
        # check if the router is none or not.
        if check_router is None:
            return exceptions.bad_request_error(f"Permission with router name: {user_permit.router_name} does not exists")
        # check if the permission is disabled.
        if not check_router.status:
            return exceptions.bad_request_error(f"Permission with router name: {user_permit.router_name} is already disabled")
        # check if the group name is none or not.
        # check the group name.
        bool_result, group_data = check_user_group(db, user_permit.group_slug)
        # check if the group is none or not.
        if not bool_result:
            return exceptions.bad_request_error(group_data)
        # check if such permission already exists for the UserGroup.
        check_user_permission = models.UserGroupPermission.userpermit_object(
            db).filter_by(user_group_id=group_data.id, permission_id=check_router.id).first()   
        if check_user_permission is not None:
            return exceptions.bad_request_error(f"Permission already exist for UserGroup")
        # else create it immediately.
        user_permit_dict = {}
        user_permit_dict['user_group_id'] = group_data.id
        user_permit_dict['permission_id'] = check_router.id
        
        new_group_permit = models.UserGroupPermission.create_usergroup_permit(user_permit_dict)
        db.add(new_group_permit)
        db.commit()
        
        return success_response.success_message([], "User Group Permission was successfully created", 201)
    except Exception as e:
        return exceptions.server_error(str(e))
    
def get_group_permissions(db, group_slug):
    try:
        # check the group name.
        bool_result, data = check_user_group(db, group_slug)
        # check if the group is none or not.
        if not bool_result:
            return exceptions.bad_request_error(data)
                
        user_permissions = models.UserGroupPermission.userpermit_object(
            db).options(
                joinedload(models.UserGroupPermission.permissions).load_only('router_name', 'label'),
                load_only('id'),
            ).filter_by(user_group_id=data.id).all()
            
        return success_response.success_message(user_permissions)
    except Exception as e:
        return exceptions.server_error(str(e))        

def remove_permission(db, group_slug, route_names):
    # for multiple and single delete or removal.
    try:
        # check the group name.
        bool_result, group_data = check_user_group(db, group_slug)
        # check if the group is none or not.
        if not bool_result:
            return exceptions.bad_request_error(group_data)
        # check user, centers and other properties.
        bool_result, data, permit_values = check_group_permission(
            db, route_names)
        
        if not bool_result:
            return exceptions.bad_request_error(data[0], data[1])
        # check if the ids exist for the usergroup in the UserGroupPermissionTable
        user_permission = models.UserGroupPermission.userpermit_object(
            db).filter(models.UserGroupPermission.user_group_id==group_data.id,
                       models.UserGroupPermission.permission_id.in_(list(permit_values.keys()))
                       )
        # check difference.
        bool_result, permit_data = check_permit_diff(db, user_permission.all(), permit_values)
        if not bool_result:
            return exceptions.bad_request_error(permit_data[0], permit_data[1])
        # remove the center ids immediately.
        user_permission.delete()
        db.commit()
        
        return success_response.success_message([], "Permission was successfully deleted for UserGroup")
    except Exception as e:
        return exceptions.server_error(detail=str(e))