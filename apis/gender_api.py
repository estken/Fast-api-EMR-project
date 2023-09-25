from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db.session import get_db
from schemas.gender_schema import (
    GenderSchema, 
    GenderUpdateSchema
)
from crud import gender_crud
from auth import validate_active_client

gender_router = APIRouter(
    prefix="/gender",
    tags=["Gender"]
)

@gender_router.post("/create", summary="Create New Gender", status_code=200)
async def create_gender(gender: GenderSchema, db: Session = Depends(get_db),
                        current_user : dict = Depends(validate_active_client)):
    
    return gender_crud.create_gender(db, gender)

@gender_router.patch("/disable/{slug}", summary="Disable a gender", status_code=200)
async def disable_group(slug: str, current_user:dict = Depends(validate_active_client), db: Session = Depends(get_db)):    
    update_data = {
        "status": False
    }
    return gender_crud.update_gender(db, slug, update_data, True)

@gender_router.patch("/enable/{slug}", summary="Enable a gender", status_code=200)
async def disable_group(slug: str, current_user:dict = Depends(validate_active_client), db: Session = Depends(get_db)):    
    update_data = {
        "status": True
    }
    return gender_crud.update_gender(db, slug, update_data, True)

@gender_router.patch("/update/{slug}", summary="Enable a gender", status_code=200)
async def disable_group(slug: str, update_data: GenderUpdateSchema, 
                        current_user:dict = Depends(validate_active_client), db: Session = Depends(get_db)):    
    
    return gender_crud.update_gender(db, slug, update_data.dict(exclude_unset=True), False)

@gender_router.get('/', summary="Get all Genders (both enabled and disabled)", status_code=200)
async def get_genders(current_user:dict = Depends(validate_active_client),
                      db: Session = Depends(get_db)):
    
    return gender_crud.get_genders(db)

@gender_router.get('/active', summary="Get all Enabled Genders ", status_code=200)
async def get_genders(current_user:dict = Depends(validate_active_client),
                      db: Session = Depends(get_db)):
    
    return gender_crud.get_active_genders(db)

@gender_router.get('/{slug}', summary="Get Single Gender Information", status_code=200)
async def get_single_gender(slug:str, current_user:dict = Depends(validate_active_client),
                      db: Session = Depends(get_db)):
    
    return gender_crud.get_single_gender(db, slug)

    
        