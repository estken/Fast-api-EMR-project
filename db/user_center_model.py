from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text
import sys
import random
sys.path.append("..")

class UserCenter(Base):
    __tablename__ = 'user_center'
    id = Column(Integer, primary_key=True, index= True)
    center_id = Column(Integer, ForeignKey("client_center.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("client_users.id"), nullable=False)
    is_default = Column(Boolean, nullable=False)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    
    # relationships.
    client_users = relationship('ClientUsers', back_populates='user_centers')
    client_centers = relationship('ClientCenter', back_populates='user_centers')
    
    # create the static methods
    @staticmethod
    def user_center_object(db):
        return db.query(UserCenter)
    
    @staticmethod
    def create_user_center(user_center_data: dict):
        return UserCenter(**user_center_data)
    
    @staticmethod
    def bulk_create(center_ids, user_id, selected_center):
        return [UserCenter(user_id=user_id, center_id=center_id, is_default=(center_id == selected_center))
                for center_id in center_ids]
            
    @staticmethod
    def get_user_center_by_id(db, user_center_id: int):
        return UserCenter.user_center_object(db).get(user_center_id)
    
    @staticmethod
    def get_user_centers(db, user_id: int):
        return UserCenter.user_center_object(db).filter_by(
            user_id=user_id).all()
        
    @staticmethod
    def update_user_center(db, user_center_id: int, user_center_data: dict):
        user_center = UserCenter.get_user_center_by_id(db, user_center_id)
        for key, value in user_center_data.items():
            setattr(user_center, key, value) 
        return user_center