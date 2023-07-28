from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db.session import get_db
from schema import (
    ClientCenterSchema,
    ClientCenterSlugSchema
)
from crud import center_crud
from auth import validate_active_client

center_router = APIRouter(
    prefix="/center",
    tags=["Client Center"],
)

@center_router.post('/create', summary="Create a Center for a client", status_code=201)
async def create_center(client_center: ClientCenterSchema, db: Session = Depends(get_db), 
                        current_user: dict= Depends(validate_active_client)):
    
    return center_crud.create_center(db, current_user, client_center)

@center_router.get('/', summary="list all centers per client", status_code=200)
async def view_center(db:Session = Depends(get_db), 
                      current_user: dict = Depends(validate_active_client)):
    
    return center_crud.get_centers(db)

@center_router.patch("/disable", summary="Disable a Client Center", status_code=200)
async def disable_center(center_slug: ClientCenterSlugSchema, db: Session = Depends(get_db),
                         current_user: dict = Depends(validate_active_client)):
    
    return center_crud.update_center_status(db, current_user, center_slug, False)

@center_router.patch("/enable", summary="Enable a Client Center", status_code=200)
async def disable_center(center_slug: ClientCenterSlugSchema, db: Session = Depends(get_db),
                         current_user: dict = Depends(validate_active_client)):
    
    return center_crud.update_center_status(db, current_user, center_slug, True)

@center_router.patch("/edit/{center_slug}", summary="Edit a Client Center", status_code=200)
async def edit_center(center_slug: str, update_center_data: ClientCenterSchema, db: Session = Depends(get_db),
                         current_user: dict = Depends(validate_active_client)):
    
    return center_crud.update_center(db, current_user, update_center_data.dict(exclude_unset=True), center_slug)

@center_router.get('/single/{center_slug}', summary="Get Single Client Center Information", status_code=200)
async def get_center(center_slug: str, db: Session = Depends(get_db),
                     current_user: dict = Depends(validate_active_client)):
    
    return center_crud.get_center(db, center_slug)