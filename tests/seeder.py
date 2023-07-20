from sqlalchemy.orm import Session
import sys
sys.path.append("..")
import uuid
from argon2 import PasswordHasher #password hashing mechanism.
        
def seed_client(db: Session):
    from db.client_model import Client
    client_data = [
        {'client_name': 'test1', 'slug': 'client-f','client_key': "new_key"},
        {'client_name': 'test1', 'slug': 'client-a','client_key': "new_key2"},
        {'client_name': 'test1', 'slug': 'client-b','client_key': "new_key3"},
        {'client_name': 'test1', 'slug': 'client-c','client_key': "new_key4"},
        {'client_name': 'test1', 'slug': 'client-d','client_key': "new_key5"},
        {'client_name': 'test1', 'slug': 'client-e','client_key': "new_key6"},
        {'client_name': 'test1', 'slug': 'client-g','client_key': "new_key7"},
        {'client_name': 'test1', 'slug': 'client-h','client_key': "new_key8"},
        {'client_name': 'test1', 'slug': 'client-i','client_key': "new_key9"},
        {'client_name': 'test1', 'slug': 'client-j','client_key': "new_key10"},
        {'client_name': 'test1', 'slug': 'client-k','client_key': "new_key11"},
        {'client_name': 'test1', 'slug': 'client-l','client_key': "new_key12"}
    ]
    
    if Client.get_client_object(db).count() == 0:
        client_instance = [Client(**client) for client in client_data]
        db.add_all(client_instance)
        db.commit()
        
def seed_client_prod(db: Session):
    from db.client_model import Client
    client_data = [
        {'client_name': 'super admin', 'slug': 'intuitive','client_key': "837b9813-0a24-44d1-924c-0762ca05a8d2"}
    ]
    
    existing_clients = db.query(Client).filter(Client.slug.in_([client['slug'] for client in client_data])).all()

    if not existing_clients:
        client_instances = [Client(**client) for client in client_data]
        db.add_all(client_instances)
        db.commit()
        
def seed_client_center(db: Session):
    from db.client_model import ClientCenter
    center_data = [
        {'client_id':1, 'center': 'client 1', 'slug': 'center-1'},
        {'client_id': 1, 'center': 'client 2', 'slug': 'center-2'},
        {'client_id': 1, 'center': 'client 3', 'slug': 'center-3'}
    ]
    
    if ClientCenter.get_center_object(db).count() == 0:
        center_instance = [ClientCenter(**center) for center in center_data]
        db.add_all(center_instance)
        db.commit()
    
def seed_client_users(db: Session):
    from db.client_model import ClientUsers
    client_user_data = [
        {'client_id':1, 'username': 'admin@intuitive.com', 'password': 'Qwerty123@', 'admin': True},
        {'client_id':2, 'username': 'ab@gmail.com', 'password': 'Qwerty123@'},
    ]
    
    if ClientUsers.client_user_object(db).count() == 0:
        user_instance = []
        hash_pw = PasswordHasher()
        for user in client_user_data:
            hashed = hash_pw.hash(user['password'])
            user['password'] = hashed
            user_instance.append(ClientUsers(**user))
              
        db.add_all(user_instance)
        db.commit()
        
def seed_client_user_prod(db: Session):
    from db.client_model import ClientUsers
    client_user_data = [
        {'client_id':1, 'username': 'admin@intuitive.com', 'password': 'Qwerty123@', 'admin': True}
    ]
    
    if ClientUsers.client_user_object(db).count() == 0:
        user_instance = []
        hash_pw = PasswordHasher()
        for user in client_user_data:
            hashed = hash_pw.hash(user['password'])
            user['password'] = hashed
            user_instance.append(ClientUsers(**user))
              
        db.add_all(user_instance)
        db.commit()
