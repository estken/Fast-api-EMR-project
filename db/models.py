# for models.
from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text
import sys
sys.path.append("..")

# Client Table.
class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    client_key = Column(String(250), unique=True, nullable=False, index=True)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # relationship
    client_users = relationship("ClientUsers", back_populates="client")
    # get the client object
    @staticmethod
    def get_client_object(db: Session):
        return db.query(Client)
                              
    # get the client by ID
    @staticmethod
    def get_client_by_id(db: Session, id: int):
        return Client.get_client_object(db).get(id)
        
    # static method to check if the key exists
    @staticmethod
    def check_single_key(db: Session, client_key):
        return Client.get_client_object(db).filter_by(client_key = client_key).first()
    
    # static method to create client.   
    @staticmethod
    def create_single_client(db: Session, slug, client_key):
        return Client(slug = slug, client_key = client_key)  
    
    @staticmethod
    def retrieve_all_client(db: Session):
        return Client.get_client_object(db).options(load_only(Client.slug, Client.status)).all()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
    # static method
    @staticmethod
    def update_single_client(db: Session, client_id, client_data): 
        client = Client.get_client_by_id(db, client_id)
        for key, value in client_data.items():
            setattr(client, key, value)
        return client
class ClientUsers(Base):
    __tablename__ = 'client_users'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete="CASCADE"), nullable=False)
    email_address = Column(String(100), nullable=False, index=True)
    password = Column(String(255), nullable=False)
    admin = Column(Boolean, default=False)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # relationships
    client = relationship("Client", back_populates="client_users")
    
    # create static methods.
    @staticmethod
    def client_user_object(db):
        return db.query(ClientUsers)
    
    @staticmethod
    def create_client_users(client_user_data: dict):
        return ClientUsers(**client_user_data)
    
    @staticmethod
    def retrieve_client_users(db, client_id):
        return ClientUsers.client_user_object(db).filter_by(client_id = client_id)
    
    @staticmethod
    def retrieve_all_users(db):
        return ClientUsers.client_user_object(db)
    
    @staticmethod
    def check_client_email(db, client_id, email_address):
        return ClientUsers.client_user_object(db).filter_by(
            client_id = client_id, email_address= email_address
        ).first()
    
    @staticmethod
    def retrieve_user_by_id(db, user_id):
        return ClientUsers.client_user_object(db).get(user_id)
    
    @staticmethod
    def update_client_user(db, user_id, update_data):
        client_user = ClientUsers.retrieve_user_by_id(db, user_id)
        for key, value in update_data.items():
            setattr(client_user, key, value)
        return client_user