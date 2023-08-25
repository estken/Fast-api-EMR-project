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

def create_user_permit(db, user_permit):
    try:
        # check if the router name already exists for client.
        check_router = models.UserGroupPermission.get_user_permit(
            db).filter_by()
        
    except Exception as e:
        return exceptions.server_error(str(e))