#access and refresh token.
from datetime import datetime, timedelta
from jose import jwt
from db.models import ClientUsers
import os
from response_handler import error_response

ACCESS_SECRET_KEY = os.getenv('ACCESS_SECRET_KEY')
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_MINUTES = 30

def create_token(users: ClientUsers, center_id = 0):
    # create the access token.
    access_token = create_access_token(users, center_id)
    # create the refresh token.
    refresh_token = create_refresh_token(users, center_id)
    # todo: generate the page_slug, as well as permission for each users.
    
    return [{
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }]        

def create_access_token(users: ClientUsers, center_id):
    # Set the expiration time for the access token.
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expiry = datetime.utcnow() + access_token_expire
    # Create the access token payload.
    access_token_payload = {
        "sub": users.username,
        "client_id": users.client_id,
        "user_id": users.id,
        "selected_id": users.client_id,
        "exp": access_token_expiry,
        "center_id": center_id
    }
    # encode the token.
    encoded_jwt = jwt.encode(access_token_payload, ACCESS_SECRET_KEY, algorithm="HS256")
    return encoded_jwt
    
def create_refresh_token(users: ClientUsers, center_id):
    # Set the expiration time for the refresh token.
    refresh_token_expire = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token_expiry = datetime.utcnow() + refresh_token_expire
    # Create the refresh token payload.
    refresh_token_payload = {
        "sub": users.username,
        "client_id": users.client_id,
        "user_id": users.id,
        "selected_id": users.client_id,
        "exp": refresh_token_expiry,
        "center_id": center_id
    }
    # encode the token.
    encoded_jwt = jwt.encode(refresh_token_payload, REFRESH_SECRET_KEY, algorithm="HS256")
    return encoded_jwt    

def verify_refresh_token(db, token: str):
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=["HS256"]) 
        # get the email and client_id
        username = payload.get("sub")
        client_id = payload.get("client_id")
        center_id = payload.get("center_id")
        # get the user model.
        get_user = ClientUsers.check_client_username(db, client_id, username)
        
        new_token = create_token(get_user, center_id)
        
    except jwt.ExpiredSignatureError:
        return False, 'Token has expired.'

    except jwt.JWTError:
        return False, "Invalid Token"
    
    except Exception as e:
        return False, str(e)
    
    return True, new_token