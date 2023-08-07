import pytest
from fastapi.testclient import TestClient
import sys
sys.path.append("..")
from db.session import engine, Base
from db.session import Session as sess
from main import access_control_app 
# the scope = 'session' is called once when the test is runned accross all files.
# The code is executed for all files
@pytest.fixture(scope='session')
def db():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

# This is called for each test function in the test files.     
@pytest.fixture(scope='function')
def get_session(db):
    connection = engine.connect()
    transaction = connection.begin()
    session = sess(bind=connection)
    # drop and re-create all tables
    Base.metadata.drop_all(bind=connection)
    Base.metadata.create_all(bind=connection)

    try:
        yield session
        session.commit()
    finally:
        session.close()
        transaction.rollback()
        connection.close()
        
@pytest.fixture(scope='function')
def client_instance():    
    with TestClient(access_control_app) as client:
        yield client

@pytest.fixture(scope='function')
def admin_details():
    return {"username": "admin@intuitive.com", "password": "Qwerty123@"}

@pytest.fixture(scope='function')
def client_header():
    return {'Client-Authorization': 'new_key'}


@pytest.fixture(scope='function')
def admin_login(get_session, client_instance, client_header, admin_details):
    from .seeder import seed_client, seed_client_users
    seed_client(get_session)
    seed_client_users(get_session)
    response = client_instance.post("/user/login", headers=client_header, data=admin_details)
    token = response.json()['data']
    return token