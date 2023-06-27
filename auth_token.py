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

def create_token(users: ClientUsers):
    # create the access token.
    access_token = create_access_token(users)
    # create the refresh token.
    refresh_token = create_refresh_token(users)
    # todo: generate the page_slug, as well as permission for each users.
    
    return [{
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }]        

def create_access_token(users: ClientUsers):
    # Set the expiration time for the access token.
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token_expiry = datetime.utcnow() + access_token_expire
    # Create the access token payload.
    access_token_payload = {
        "sub": users.email_address,
        "client_id": users.client_id,
        "user_id": users.id,
        "exp": access_token_expiry
    }
    # encode the token.
    encoded_jwt = jwt.encode(access_token_payload, ACCESS_SECRET_KEY, algorithm="HS256")
    return encoded_jwt
    
def create_refresh_token(users: ClientUsers):
    # Set the expiration time for the refresh token.
    refresh_token_expire = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token_expiry = datetime.utcnow() + refresh_token_expire
    # Create the refresh token payload.
    refresh_token_payload = {
        "sub": users.email_address,
        "client_id": users.client_id,
        "user_id": users.id,
        "exp": refresh_token_expiry
    }
    # encode the token.
    encoded_jwt = jwt.encode(refresh_token_payload, REFRESH_SECRET_KEY, algorithm="HS256")
    return encoded_jwt    

def verify_refresh_token(db, token: str):
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=["HS256"]) 
        # get the email and client_id
        email = payload.get("sub")
        client_id = payload.get("client_id")
        # get the user model.
        get_user = ClientUsers.check_client_email(db, client_id, email)
        
        new_token = create_token(get_user)
        
    except jwt.ExpiredSignatureError:
        return error_response.unauthorized_error(detail='Token has expired.')

    except jwt.JWTError:
        return error_response.unauthorized_error(detail="Invalid Token")
    
    except Exception as e:
        return error_response.unauthorized_error(detail=str(e))
    
    return new_token