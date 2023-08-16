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
    id = Column