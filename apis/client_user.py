from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import sys
sys.path.append("..")
from db.session import get_db
from schema import (
    ClientUserSchema, 
    UpdateClientUserSchema,
    refreshTokenSchema,
    UpdateClientUserSchema
)
from crud import user_crud
from auth import validate_client_key
from auth import validate_active_client
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter(
    prefix="/user",
    tags=["Users"],
)

@user_router.post("/login", summary="Login into the Client user account", status_code=200, dependencies=[Depends(validate_client_key)])
async def user_login(request: Request, login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # get the client id
    client_id = request.state.data
    # get the email and password.
    user_email = login_data.username
    user_password = login_data.password
    
    return user_crud.user_login(db, client_id, user_email, user_password)

@user_router.post("/create", summary="Create a new User for the client", status_code=201)
def create_new_user(new_user: ClientUserSchema, db: Session = Depends(get_db), 
                    current_user:dict = Depends(validate_active_client)):
    
    return user_crud.create_user(db, current_user, new_user)


@user_router.post("/admin/login", summary="Login into the Client user account", status_code=200, dependencies=[Depends(validate_client_key)])
async def user_login(request: Request, login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # get the client id
    client_id = request.state.data
    # get the email and password.
    user_email = login_data.username
    user_password = login_data.password
    
    return user_crud.admin_login(db, client_id, user_email, user_password)

@user_router.post("/refresh/token", summary="Refresh Expired token of logged in users.", status_code=200)
async def refresh_token(refresh_token: refreshTokenSchema, db: Session = Depends(get_db)):
    return user_crud.refresh_token(db, refresh_token.refresh_token)

@user_router.get('/view', summary="View Single User Information", status_code=200)
async def view_detail(current_user:dict = Depends(validate_active_client), db: Session = Depends(get_db)):
    return user_crud.get_details(db, current_user)

@user_router.patch('/update/{username}', summary="Update the User Information", status_code=200)
async def update_user(username: str, update_data: UpdateClientUserSchema, current_user : dict = Depends(validate_active_client), 
                      db: Session = Depends(get_db)):
    return user_crud.update_details(db, username, current_user, update_data)
    
    