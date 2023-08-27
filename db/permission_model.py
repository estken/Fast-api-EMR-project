from .session import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, relationship
from datetime import datetime
import sys
sys.path.append("..")
from db.session import Session as sess

db = sess()

class Permissions(Base):
    __tablename__='permissions'
    id = Column(Integer, primary_key=True, index=True)
    router_name = Column(String(100), nullable=False, unique=True, index=True)
    label = Column(String(100), nullable=False, unique=True)
    description = Column(TEXT)
    status = Column(Boolean, default=True)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # create the static methods
    @staticmethod
    def permission_object(db):
        return db.query(Permissions)
    
    @staticmethod
    def get_permission_by_id(db, permit_id: int):
        return Permissions.permission_object(db).get(permit_id)
    
    @staticmethod
    def create_permission(permit_data: dict):
        return Permissions(**permit_data)
    
    @staticmethod
    def get_all_permission(db):
        return Permissions.permission_object(db).all()
    
    @staticmethod
    def get_permission_by_name(db, router_name):
        return Permissions.permission_object(db).filter_by(
            router_name=router_name).first()
        
    @staticmethod
    def update_permission(db, permit_id: int, permit_data: dict):
        permit = Permissions.get_permission_by_id(db, permit_id)
        for key, value in permit_data.items():
            setattr(permit, key, value) 
        return permit
    
    