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
    
    departments_type_rel = relationship("DepartmentModel", back_populates="department_model_type_rel")
    
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
    
    

class gender_type_model(Base):
    __tablename__ = "gender_type"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    
    
    gender_type_model_rel = relationship("DepartmentModel", back_populates="department_models_gender_rel")
    
    # get the gender type object
    @staticmethod
    def get_gender_type_object(db: Session):
        return db.query(gender_type_model)
                               
    # get the gender by ID
    @staticmethod
    def get_gender_type_by_id(db: Session, id: int):
        return gender_type_model.get_gender_type_object(db).get(id)
    
    @staticmethod
    def retrieve_all_gender(db: Session):
        return gender_type_model.get_gender_type_by_id(db).options(load_only(gender_type_model.slug)).all()
    
    @staticmethod
    # check single gender type 
    def check_single_slug(db:Session, slug:str):
        return db.query(gender_type_model).filter_by(slug=slug).first()
    
    
# department model
class DepartmentModel(Base):
    __tablename__ = "departmentsmodels"
    id = Column(Integer, primary_key=True , index=True)
    department_name = Column(String(100), unique=True)
    description = Column(String(100))
    department_type = Column(Integer, ForeignKey("departments_type.id"))
    gender = Column(Integer, ForeignKey("gender_type.id"))
    status = Column(Boolean , default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    
    department_model_type_rel = relationship("Departments_type_Model", back_populates="departments_type_rel")
    department_models_gender_rel = relationship("gender_type_model", back_populates="gender_type_model_rel")
    
    
        # static methods files
    
    # get the departments object
    @staticmethod
    def get_departments_object(db: Session):
        return db.query(DepartmentModel)
                               
    # get the departments by ID
    @staticmethod
    def get_departments_by_id(db: Session, id: int):
        return DepartmentModel.get_departments_object(db).get(id)
    
    @staticmethod
    def retrieve_all_departments(db: Session):
        return DepartmentModel.get_departments_object(db).options(load_only(DepartmentModel.department_name)).all()
    
    @staticmethod
    def create_single_departments(db:Session, departments_name:str, description:str, gender:int,department_type:int):
        return DepartmentModel(
            departments_name = departments_name,
            description = description,
            gender = gender,
            department_type = department_type
        )
        
    @staticmethod
    def view_all_departments(db:Session):
        return db.query(DepartmentModel).all()
        