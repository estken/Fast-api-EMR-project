from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text
import sys
sys.path.append("..")


class ClientUsers(Base):
    __tablename__ = 'client_users'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id', ondelete="CASCADE"), nullable=False)
    username = Column(String(100), nullable=False, index=True)
    password = Column(String(255), nullable=False)
    admin = Column(Boolean, default=False)
    status = Column(Boolean, default=True)
    is_reset = Column(Boolean, default = False)
    is_locked = Column(Boolean, default = False)
    invalid_password = Column(Integer, nullable=False, default=0)
       
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # relationships
    client = relationship("Client", back_populates="client_users")
    user_centers = relationship("UserCenter", back_populates="client_users")
    
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
    def check_client_username(db, client_id, username):
        return ClientUsers.client_user_object(db).filter_by(
            client_id = client_id, username=username
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
