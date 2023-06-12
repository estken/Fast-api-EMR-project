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
