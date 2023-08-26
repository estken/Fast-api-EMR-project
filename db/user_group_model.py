from .session import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Float, JSON, TEXT
from sqlalchemy.orm import Session
from datetime import datetime
import sys
sys.path.append("..")



class UserGroup(Base):
    __tablename__ = 'user_group'
    id = Column(Integer, primary_key=True, index=True)
    group_name = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True)
    status = Column(Boolean, nullable=False, default=True)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    
    # static methods.
    @staticmethod
    def user_group_object(db: Session):
        return db.query(UserGroup)
    
    # get the user group by ID
    @staticmethod
    def get_user_group_by_id(db: Session, id: int):
        return UserGroup.user_group_object(db).get(id)
    
    @staticmethod
    def create_user_group(user_group: dict):
        return UserGroup(**user_group)
    
    @staticmethod
    def check_slug(db, slug):
        return UserGroup.user_group_object(db).filter_by(
            slug=slug).first()
    
    @staticmethod
    def get_user_groups(db: Session):
        return UserGroup.user_group_object(db)
    
    @staticmethod
    def update_user_group(db: Session, user_group_id: int, user_group_data: dict):
        user_group = UserGroup.get_user_group_by_id(db, user_group_id)
        for key, value in user_group_data.items():
            setattr(user_group, key, value)
        return user_group