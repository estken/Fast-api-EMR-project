from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text
import sys
sys.path.append("..")

class ClientEquipment(Base):
    __tablename__="client_equipment"
    id = Column(Integer, primary_key=True, index= True)
    equipment = Column(String(100), nullable = False)
    slug = Column(String(100), default=str(uuid.uuid4()), unique=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)

    @staticmethod
    def insert_equipment(session: Session, insert_data):
        return session.add(ClientEquipment(**insert_data))
    
    @staticmethod
    def lookup_eqipment_by_slug(session: Session, slug: str):
        return session.query(ClientEquipment).filter(ClientEquipment.slug == slug).first()
    
    @staticmethod
    def lookup_eqipment_by_name(session: Session, name: str):
        return session.query(ClientEquipment).filter(ClientEquipment.equipment == name).first()
    
    @staticmethod
    def get_all_client_equipment(session: Session):
        return session.query(ClientEquipment).all()
    