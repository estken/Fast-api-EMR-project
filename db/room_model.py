from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime
from sqlalchemy.sql import text
import sys
sys.path.append("..")
from db.session import Session as sess


class ClientRoom(Base):
    __tablename__="client_rooms"
    id = Column(Integer, primary_key=True, index= True)
    center_id = Column(Integer, ForeignKey("client_center.id"), nullable=False)
    name = Column(String(100), nullable = False)
    description = Column(String(100))
    slug = Column(String(100), default=str(uuid.uuid4()), unique=True)
    status = Column(Boolean, default= True)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)

    @staticmethod
    def insert_room(session: Session, insert_data):
        return session.add(ClientRoom(**insert_data))
    
    @staticmethod
    def get_first_room(session: Session, center_id: int, room: str):
        return session.query(ClientRoom).filter(ClientRoom.center_id == center_id, ClientRoom.slug == room)
    
    @staticmethod
    def get_center_rooms(session: Session, center_id: int):
        return session.query(ClientRoom).filter(ClientRoom.center_id).all()
    
    @staticmethod
    def get_center_rooms_by_status(session: Session, center_id: int, status: int):
        return session.query(ClientRoom).filter(ClientRoom.center_id == center_id, ClientRoom.status == status).all()
    

