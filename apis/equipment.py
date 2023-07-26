from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import sys, asyncio
sys.path.append("..")
from db.session import get_db
from schemas.room_schema import EquipmentCreateBase, EquipmentNameBase, EquipmentSlugBase
from crud.room_crud import create_client_equipment, update_client_equipment, get_single_equipment, list_client_equipment, delete_client_equipment
from auth import validate_active_client


equipment_router = APIRouter(
    prefix="/equipment",
    tags=["Equipment","Room"],
)

@equipment_router.post("/create", summary="Create client equipment", status_code=201)
def create_new_equipment(gadgets: EquipmentCreateBase, db: Session = Depends(get_db), 
                    current_user_dict:dict = Depends(validate_active_client)):
    return create_client_equipment(db, gadgets)

@equipment_router.patch('/update', summary="Update equipment name", status_code=200)
async def update_user(gadget: EquipmentNameBase, current_user_dict : dict = Depends(validate_active_client), 
                      db: Session = Depends(get_db)):
    return update_client_equipment(db, gadget)

@equipment_router.get('view/{slug}', summary="View single equipment", status_code=200)
async def view_single_quipment(slug: str, current_user : dict = Depends(validate_active_client), 
                      db: Session = Depends(get_db)):
    gadget_dict = {'slug': slug } 
    client_gadget = EquipmentSlugBase(**gadget_dict)
    return get_single_equipment(db, client_gadget)

@equipment_router.get('/', summary="View all equipment", status_code=200)
async def view_all(current_user : dict = Depends(validate_active_client), 
                      db: Session = Depends(get_db)):
    return list_client_equipment(db)

@equipment_router.delete('/delete', summary="View single equipment", status_code=200)
async def deleteequipment(gadget: EquipmentSlugBase, current_user_dict : dict = Depends(validate_active_client), 
                      db: Session = Depends(get_db)):
    return delete_client_equipment(db, gadget)