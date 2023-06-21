from sqlalchemy.orm import Session
import sys
sys.path.append("..")
import uuid
        
def seed_client(db: Session):
    from db.models import Client
    client_data = [
        {'slug': 'client-f','client_key': "new_key"},
        {'slug': 'client-a','client_key': "new_key2"},
        {'slug': 'client-b','client_key': "new_key3"},
        {'slug': 'client-c','client_key': "new_key4"},
        {'slug': 'client-d','client_key': "new_key5"},
        {'slug': 'client-e','client_key': "new_key6"},
        {'slug': 'client-g','client_key': "new_key7"},
        {'slug': 'client-h','client_key': "new_key8"},
        {'slug': 'client-i','client_key': "new_key9"},
        {'slug': 'client-j','client_key': "new_key10"},
        {'slug': 'client-k','client_key': "new_key11"},
        {'slug': 'client-l','client_key': "new_key12"}
    ]
    
    if Client.get_client_object(db).count() == 0:
        client_instance = [Client(**client) for client in client_data]
        db.add_all(client_instance)
        db.commit()
        
def seed_client_prod(db: Session):
    from db.models import Client
    client_data = [
        {'slug': 'intuitive','client_key': "intuitive_key"}
    ]
    
    existing_clients = db.query(Client).filter(Client.slug.in_([client['slug'] for client in client_data])).all()

    if not existing_clients:
        client_instances = [Client(**client) for client in client_data]
        db.add_all(client_instances)
        db.commit()

def seed_user_group(db: Session):
    from db.models import UserGroup
    user_group_data = [
        {'client_id': 1, 'slug': 'slug', 'group_name': 'admin'},
        {'client_id': 1, 'slug': 'slug2', 'group_name': 'doctor', 'status': False},
        {'client_id': 2, 'slug': 'slug3', 'group_name': 'pharmacy'},
        {'client_id': 2, 'slug': 'slug4', 'group_name': 'nurse'},
        {'client_id': 1, 'slug': 'slug5', 'group_name': 'admin1'},
        {'client_id': 1, 'slug': 'slug6', 'group_name': 'doctor1', 'status': False},
        {'client_id': 2, 'slug': 'slug7', 'group_name': 'pharmacy1'},
        {'client_id': 2, 'slug': 'slug8', 'group_name': 'nurse1'},
        {'client_id': 1, 'slug': 'slug9', 'group_name': 'admin2'},
        {'client_id': 1, 'slug': 'slug10', 'group_name': 'doctor2', 'status': False},
        {'client_id': 2, 'slug': 'slug11', 'group_name': 'pharmacy2'},
        {'client_id': 2, 'slug': 'slug12', 'group_name': 'nurse3'},
        {'client_id': 2, 'slug': 'slug13', 'group_name': 'pharmacy3'},
        {'client_id': 2, 'slug': 'slug14', 'group_name': 'nurse4'}, 
        {'client_id': 2, 'slug': 'slug15', 'group_name': 'pharmacy4'},
        {'client_id': 2, 'slug': 'slug16', 'group_name': 'nurse5'},
        {'client_id': 2, 'slug': 'slug17', 'group_name': 'pharmacy5'},
        {'client_id': 2, 'slug': 'slug18', 'group_name': 'nurse6'}
    ]
    
    if UserGroup.user_group_object(db).count() == 0:
        group_instance = [UserGroup(**user_group) for user_group in user_group_data]
        db.add_all(group_instance)
        db.commit()