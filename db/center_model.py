from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text
import sys
sys.path.append("..")

class ClientCenter(Base):
    __tablename__="client_center"
    id = Column(Integer, primary_key=True, index= True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    center = Column(String(100), nullable = False)
    slug = Column(String(100), nullable = False, unique=True)
    status = Column(Boolean, default= True)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # relationship part.
    client = relationship('Client', back_populates="client_centers")
    
    def __init__(self, center, client_id, status):
        self.center = center
        self.client_id = client_id
        self.status = status
        self.slug = self.generate_slug(self.center[:10] + str(self.client_id))
        
    def generate_slug(self):
        
        
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