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
    users = relationship("UserGroup", back_populates="clients")
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
    
class UserGroup(Base):
    __tablename__ = 'user_group'
    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete='CASCADE'))
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    
    # relationship.
    clients = relationship("Client", back_populates="users")
    # static methods.
    @staticmethod
    def user_group_object(db: Session):
        return db.query(UserGroup)
    
    # get the user group by ID
    @staticmethod
    def get_user_group_by_id(db: Session, id: int):
        return UserGroup.user_group_object(db).get(id)
    @staticmethod
    def create_user_group(user_group: dict):
        return UserGroup(**user_group)
    
    @staticmethod
    def get_user_groups(db: Session):
        return UserGroup.user_group_object(db).distinct(UserGroup.group_name, UserGroup.slug)
    
    @staticmethod
    def get_client_user_groups(db: Session, client_id: int):
        return UserGroup.user_group_object(db).filter_by(client_id=client_id)
    
    @staticmethod
    def update_user_group(db: Session, user_group_id: int, user_group_data: dict):
        user_group = UserGroup.get_user_group_by_id(db, user_group_id)
        for key, value in user_group_data.items():
            setattr(user_group, key, value)
        return user_group
           
