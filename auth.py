# for authorizaton process.
from fastapi import Depends, HTTPException, Request
from db.session import get_db
from sqlalchemy.orm import Session
from db import models
from jose import jwt
from response_handler import error_response
from fastapi.security import OAuth2PasswordBearer
from crud.user_crud import check_password_stat

import os

ACCESS_SECRET_KEY = os.getenv('ACCESS_SECRET_KEY')
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')

# Create an instance of the OAuth, redirects the user back here.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'user/login')


async def validate_client_key(request: Request, db: Session=Depends(get_db)):
    # get the client key from the header.
    get_client_key = request.headers.get("Client-Authorization")
    # if the client key is missing throw an exception.
    if not get_client_key:
        return error_response.unauthorized_error(detail="Client key is missing")
    # check if the client key is valid.
    get_client = models.Client.check_single_key(db, get_client_key)
    if get_client is None:
        return error_response.unauthorized_error(detail="Client details not found")
    # client is inactive
    if get_client.status is False:
        return error_response.unauthorized_error(detail="Inactive account")
    # Store the data in the request state
    request.state.data = get_client.id
    
    return request

async def validate_active_client(db: Session = Depends(get_db), token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=["HS256"])
        # get username, client_id.
        username = payload.get("sub")
        client_id = payload.get("client_id")
        # check if the client mail exist for that user.
        get_user = models.ClientUsers.check_client_username(db, client_id, username)
        if get_user is None:
            return error_response.unauthorized_error(detail="You don't have permission to this page")
        # check if the user's account is inactive
        if not get_user.status:
            return error_response.forbidden_error(detail="Your account is inactive")
        # check if the client account is inactive.
        if not get_user.client.status:
            return error_response.forbidden_error(detail="Client is inactive")
        # check if the account requires password reset or change.
        bool_result, message = check_password_stat(get_user)
        if not bool_result:
            return error_response.forbidden_error(data=message)
    # jwt token error
    except jwt.ExpiredSignatureError:
        return error_response.unauthorized_error(detail='Token has expired.')
        
    except jwt.JWTError:
        return error_response.unauthorized_error(detail="Invalid Token")
    
    except Exception as e:
        return error_response.unauthorized_error(detail=str(e))
    
    return get_user