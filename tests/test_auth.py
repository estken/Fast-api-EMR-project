import json
from .conftest import get_session
from db.client_model import Client
from db.user_model import ClientUsers 
from .seeder import seed_client, seed_client_users

def test_login(get_session, client_instance, admin_details, client_header):
    seed_client(get_session)
    seed_client_users(get_session)
    response = client_instance.post("/user/login", headers= client_header, data=admin_details)
    assert response.status_code == 200
    token = response.json()['data']['access_token']
    refresh_token = response.json()['data']['refresh_token']
    assert token is not None
    assert refresh_token is not None
    return token
