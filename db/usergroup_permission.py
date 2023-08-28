from .session import Base
from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import sys
sys.path.append("..")


class UserGroupPermission(Base):
    __tablename__ = "usergroup_permission"
    id = Column(Integer, primary_key= True, index= True)
    permission_id = Column(Integer, ForeignKey('permissions.id', ondelete="CASCADE"), nullable=False)
    user_group_id = Column(Integer, ForeignKey('user_group.id', ondelete="CASCADE"), nullable=False)
    
    created_at = Column(TIMESTAMP(timezone=True),
                        default = datetime.utcnow(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=datetime.utcnow(), 
                        onupdate=datetime.utcnow(), nullable=False)
    # define the relationships.
    permissions = relationship("Permissions", back_populates="user_permission")
    user_group = relationship("UserGroup", back_populates="user_permission")
    # define the static methods.
    @staticmethod
    def userpermit_object(db):
        return db.query(UserGroupPermission)
    
    @staticmethod
    def create_usergroup_permit(user_permit_data: dict):
        return UserGroupPermission(**user_permit_data)
    
    @staticmethod
    def get_user_permit(db, user_group_id):
        return UserGroupPermission.userpermit_object(db).filter_by(
            user_group_id)
    
    @staticmethod
    def check_single_permit(db, permit_id):
        return UserGroupPermission.userpermit_object(db).get(permit_id)
    
    @staticmethod
    def update_user_permit(db, permit_id, permit_update_data):
        user_permit = UserGroupPermission.check_single_permit(db, permit_id)
        for key, value in permit_update_data.items():
            setattr(user_permit, key, value)
        return user_permit
        
    
    
