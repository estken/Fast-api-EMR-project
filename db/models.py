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
    # relationship.
    client_centers = relationship('ClientCenter', back_populates='client')
    
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
    
class ClientCenter(Base):
    __tablename__="client_center"
    id = Column(Integer, primary_key=True, index= True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    center = Column(String(100), nullable = False)
    status = Column(Boolean, default= True)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # relationship part.
    client = relationship('Client', back_populates="client_centers")
    
    @staticmethod
    def get_center_object(db: Session):
        return db.query(ClientCenter)
    
    @staticmethod
    def get_center_by_id(db: Session, center_id: int):
        return ClientCenter.get_center_object(db).get(center_id)
    
    @staticmethod
    def create_center(center_data: dict):
        return ClientCenter(**center_data)
    
    @staticmethod
    def get_all_client_center(db: Session, client_id: int):
        return ClientCenter.get_center_object(db).filter_by(client_id = client_id).all()
    
    @staticmethod
    def get_all_center(db: Session):
        return ClientCenter.get_center_object(db).all()
    
    @staticmethod
    def update_center(db:Session, center_id: int, update_data):
        client_center = ClientCenter.get_center_by_id(db, center_id)
        for key, value in update_data.items():
            setattr(client_center, key, value)
        return client_center