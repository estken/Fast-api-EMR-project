from fastapi import APIRouter, Depends, Request, HTTPException, Query
from sqlalchemy.orm import Session
import sys, asyncio
sys.path.append("..")
from db.session import get_db
from schema import ClientSchema, UpdateStatusSchema, UpdateClientKeySchema
from crud import client_crud
from db import client_model as models
from auth import validate_client_key, validate_active_client
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

client_router = APIRouter(
    prefix="/client",
    tags=["client"],
)
                                                                                                                                                                                                                                                                                                                                                                                                                                     
@client_router.post("/create", summary="create a single client", status_code=201)
async def create_new_client(client_details: ClientSchema, db: Session = Depends(get_db)):
    return client_crud.create_new_client(db, client_details)

@client_router.patch("/deactivate", summary="deactivate a client", status_code=200, dependencies=[Depends(validate_client_key)])
async def deactivate_client(request: Request, db: Session= Depends(get_db)):
    # get the request client data returned from the middleware.
    client_id = request.state.data
    # set the status to False.
    update_data = {
        "status": False
    }
    return client_crud.update_client(db, client_id, UpdateStatusSchema(**update_data))
    
@client_router.patch('/reactivate/{client_id}', summary="Reactivate a client", status_code=200)
async def reactivate_client(client_id: int, db: Session= Depends(get_db)):
    update_data = {
        "status": True
    }
    return client_crud.update_client(db, client_id, UpdateStatusSchema(**update_data))

@client_router.patch('/update', summary="Update single client key", status_code=200, dependencies=[Depends(validate_client_key)])
async def update_client_key(request: Request, client_key: UpdateClientKeySchema, db: Session = Depends(get_db)):
    # get the request client data returned from the middleware.
    client_id = request.state.data
    return client_crud.update_client_key(db, client_id, client_key)

@client_router.get('/', summary="Get all clients status and slugname", status_code=200)
async def get_all_client(page: int = Query(1, ge=1), page_size: int = 10, db: Session=Depends(get_db)):
    return client_crud.get_all_clients(db, page, page_size)

@client_router.post('/change/{client_slug}', summary="Select or change to another client", status_code=200)
async def change_client(client_slug: str, 
                        db: Session = Depends(get_db), current_user: dict = Depends(validate_active_client)):
    
    return client_crud.change_client(db, client_slug, current_user)