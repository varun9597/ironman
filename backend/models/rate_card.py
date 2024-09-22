from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.items import Item
from models.society import Society
from models.user import User
import datetime

Base = declarative_base()

class RateCard(Base):
    __tablename__ = 'tbl_rate_card'

    rate_id = Column("pk_rate_id", Integer, primary_key=True, autoincrement=True)
    item_id = Column("fk_item_id", Integer, ForeignKey('tbl_items.pk_item_id'))
    user_id = Column("fk_user_id", Integer, ForeignKey('tbl_users.id'))
    society_id = Column("fk_soc_id", Integer, ForeignKey('tbl_society.pk_soc_id'))
    rate = Column(Numeric(5, 1), nullable=False, default=0.0)
    insert_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    is_active = Column(String(10), nullable=False, default='Y')

    # Relationships
    item = relationship('Item', backref='rate_cards')
    user = relationship('User', backref='rate_cards')
    society = relationship('Society', backref='rate_cards')

    def __repr__(self):
        return f"<RateCard(pk_rate_id={self.pk_rate_id}, rate={self.rate})>"
