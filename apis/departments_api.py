from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
import sys
from typing import List
sys.path.append("..")
from db.session import get_db
from schema import CreateDepartmentTypeSchema
from crud.depratments_crud import create_department_type
from auth import validate_active_client

# router configuration
user_departments_router = APIRouter(
    prefix="/departments",
    tags=["User Departments"],
)

# endpoint to create department type
@user_departments_router.post("/create/department_type", summary="create a department type", status_code=201)
async def create_new_department_type(create: CreateDepartmentTypeSchema, db: Session = Depends(get_db)):
    return create_department_type(db,create)

