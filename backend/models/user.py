from sqlalchemy import Column, Integer, String, Boolean,Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'tbl_users'
    
    user_id = Column("id",Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(String(10), nullable=False, default='Y')
    role = Column(Enum('resident', 'laundry-personnel', 'admin', name="user_roles"), nullable=False, default='resident')

    def __repr__(self):
        return f"<User(id={self.user_id}, name={self.name}, username={self.username}, role={self.role})>"

