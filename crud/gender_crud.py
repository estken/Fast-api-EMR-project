import sys
sys.path.append("..")
from utils import *
from db import client_model as models
from db.session import Session
from fastapi_pagination import Params
from response_handler import error_response as exceptions
from response_handler import success_response
from fastapi_pagination.ext.sqlalchemy import paginate
from slugify import slugify


from sqlalchemy.orm import load_only

db = Session()

def generate_slug(db, gender_slug):
    counter = 1
    base_slug = slugify(f"{gender_slug}")
    slug = base_slug
    while models.GenderModel.check_gender_slug(db, slug) is not None:
        counter += 1
        slug = f"{base_slug}{counter}"
        
    return slug


def create_gender(db, gender_data):
    try:
        # first check if the name already exists.
        check_gender = models.GenderModel.create_gender_object(
            db).filter_by(name=gender_data.name).first()
        if check_gender is not None:
            return exceptions.bad_request_error(f"Gender with name {gender_data.name} already exists!")
        # get the slug
        gender_slug = generate_slug(db, gender_data.name.lower())
        # convert the gender_data to dictionary
        gender_dict = gender_data.dict(exclude_unset=True)
        gender_dict['slug'] = gender_slug
        # create the gender.
        create_new_gender = models.GenderModel.create_gender(gender_dict)
        
        if create_new_gender is None:
            return exceptions.bad_request_error("An error ocurred while creating Gender, Please try again")  
        
        db.add(create_new_gender)
        db.commit()
        
        return success_response.success_message([], "Gender was successfully created", 201)

    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
def update_gender(db, gender_slug, update_data, check_state=False):
    try:
        # first check if the user_slug exists for that client.
        get_slug = models.GenderModel.create_gender_object(db).filter_by(
            slug= gender_slug.lower()).first()
        if get_slug is None:
            return exceptions.bad_request_error(
                f'No Gender found with Slug Name :{gender_slug}')
            
        # check if it has already been enabled or disabled.
        if check_state:
            if get_slug.status == update_data['status']:
                if get_slug.status:
                    return exceptions.bad_request_error("Gender already enabled")
                return exceptions.bad_request_error("Gender already disabled")    
        
        # update right away.
        updated_gender = models.GenderModel.update_single_gender(db, get_slug.id, update_data)
        if not updated_gender:
            return exceptions.bad_request_error("An error occurred while updating Gender")
        # update.
        db.add(updated_gender)
        db.commit()
        db.refresh(updated_gender)
        
        return success_response.success_message(updated_gender, "Gender was successfully updated")

    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
def get_genders(db):
    try:
        genders = models.GenderModel.create_gender_object(db).all()
        return success_response.success_message(genders)
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))
    
def get_active_genders(db):
    try:
        active_genders = models.GenderModel.create_gender_object(
            db).filter_by(status=True).all()
        return success_response.success_message(active_genders)
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))

def get_single_gender(db, gender_slug):
    try:
        check_gender = models.GenderModel.check_gender_slug(db, gender_slug)
        if check_gender is None:
            return exceptions.bad_request_error(
                f'No Gender found with Slug Name :{gender_slug}')
            
        return success_response.success_message(check_gender)
        
    except Exception as e:
        return exceptions.server_error(detail=str(e))