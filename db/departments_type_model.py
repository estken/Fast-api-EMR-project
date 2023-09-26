from .session import Base
from sqlalchemy import Column, Enum, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session, load_only, relationship
import uuid
from datetime import datetime

import sys
sys.path.append("..")


class Departments_type_Model(Base):
    __tablename__ = "departments_type"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    
    # get the departments type object
    @staticmethod
    def get_departments_type_object(db: Session):
        return db.query(Departments_type_Model)
                               
    # get the departments by ID
    @staticmethod
    def get_departments_type_by_id(db: Session, id: int):
        return Departments_type_Model.get_departments_type_object(db).get(id)
    
    @staticmethod
    def retrieve_all_departments(db: Session):
        return Departments_type_Model.get_departments_type_object(db).options(load_only(Departments_type_Model.slug)).all()
    
    @staticmethod
    # check single department type 
    def check_single_slug(db:Session, slug:str):
        return db.query(Departments_type_Model).filter_by(slug=slug).first()
    
    
    @staticmethod
    # create single departments type
    def create_departments_type(db:Session, slug:str):
        return Departments_type_Model(slug=slug)
    
    

        