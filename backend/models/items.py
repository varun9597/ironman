from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.user import User

Base = declarative_base()

class Item(Base):
    __tablename__ = 'tbl_items'
    
    item_id = Column("pk_item_id", Integer, primary_key=True, autoincrement=True)
    item_name = Column(String(255), nullable=False)
    user_id = Column("fk_user_id", Integer, ForeignKey('tbl_users.id'), nullable=False)
    is_active = Column(String(10), nullable=False, default='Y')

    # Relationship to user
    user = relationship('User', backref='items')

    def __repr__(self):
        return f"<Item(pk_item_id={self.pk_item_id}, item_name={self.item_name})>"
