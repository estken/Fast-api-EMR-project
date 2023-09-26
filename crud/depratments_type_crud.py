import sys
sys.path.append("..")
from utils import *
from db import departments_model as models
from db.session import Session
from fastapi_pagination import Params
from response_handler import error_response as exceptions
from response_handler import success_response
from fastapi_pagination.ext.sqlalchemy import paginate
from schema import CreateDepartmentTypeSchema,CreateDepartmentSchema

from sqlalchemy.orm import load_only

db = Session()

def create_department_type(db:Session, create:CreateDepartmentTypeSchema):
    # check if departments already exits
    check_dpt_type = models.Departments_type_Model.check_single_slug(db, slug = create.slug)
    if check_dpt_type is not None:
        return exceptions.bad_request_error("departments type already exits")
    
    create_dpt = models.Departments_type_Model.create_departments_type(db, create.slug)
    db.add(create_dpt)
    db.commit()
    db.refresh(create_dpt)
    

# crud to create single user departments

def create_departments(db:Session, create_dpt :CreateDepartmentSchema):
    #check if departments type exits
    check_dpt_type = models.Departments_type_Model.check_single_slug(db, slug=create_dpt.department_type)
    if check_dpt_type is None:
        return exceptions.bad_request_error("department type does not exits")
    department_type = check_dpt_type.slug
    
    #check gender
    check_gender = models.gender_type_model.check_single_slug(db, slug=create_dpt.gender)
    if check_gender is None:
        return exceptions.bad_request_error("No gender found")
    
    gender = check_gender.slug
    
    # create a department for each user
    
    create_data = models.DepartmentModel.create_single_departments(db,
                                                                   departments_name=create_dpt.department_name,
                                                                   description=create_dpt.description,
                                                                   gender=gender,
                                                                   department_type=department_type)
    db.add(create_data)
    db.commit()
    db.refresh(create_data)
    
    
    
# view all departments created crud
def view_all_department(db:Session):
    try:
        get_departments = models.DepartmentModel.view_all_departments(db)
        return success_response.success_message(get_departments)
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
    
    
# update departments crud
def update_departments(db:Session):
    pass