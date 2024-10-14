from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.user import User  # Import the User model for relationship
from models.base_model import Base  # Assuming Base is defined in base_model.py

class Society(Base):
    __tablename__ = 'tbl_society'
    
    society_id = Column("pk_soc_id", Integer, primary_key=True, autoincrement=True)
    soc_name = Column(String(255), nullable=False)
    user_id = Column("fk_user_id", Integer, ForeignKey('tbl_users.id'), nullable=True)
    is_active = Column(String(10), nullable=False, default='Y')

    # Relationship with User model
    user = relationship('User', back_populates='societies')

    def __repr__(self):
        return f"<Society(society_id={self.society_id}, soc_name={self.soc_name}, user_id={self.user_id})>"
