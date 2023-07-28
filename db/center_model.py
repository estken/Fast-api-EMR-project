from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text
import sys
sys.path.append("..")
from db.session import Session as sess

db = sess()

class ClientCenter(Base):
    __tablename__="client_center"
    id = Column(Integer, primary_key=True, index= True)
    center = Column(String(100), nullable = False)
    slug = Column(String(100), nullable = False, unique=True)
    status = Column(Boolean, default= True)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # relationship part.
    user_centers = relationship('UserCenter', back_populates="client_centers")
    rooms = relationship('ClientRoom', back_populates="center")
        
    @staticmethod
    def get_center_object(db: Session):
        return db.query(ClientCenter)
    
    @staticmethod
    def check_slug(db: Session, slug: str):
        return ClientCenter.get_center_object(db).filter_by(
            slug=slug
        ).first()
    
    @staticmethod
    def get_center_by_id(db: Session, center_id: int):
        return ClientCenter.get_center_object(db).get(center_id)
    
    @staticmethod
    def create_center(center_data: dict):
        return ClientCenter(**center_data)
    
    @staticmethod 
    def get_all_active_center(db: Session, status):
        return ClientCenter.get_center_object(db).filter_by(status = status).all()
    
    @staticmethod
    def get_all_center(db: Session):
        return ClientCenter.get_center_object(db).all()
    
    @staticmethod
    def update_center(db:Session, center_id: int, update_data):
        client_center = ClientCenter.get_center_by_id(db, center_id)
        for key, value in update_data.items():
            setattr(client_center, key, value)
        return client_center