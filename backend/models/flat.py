from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.society import Society
from models.customer import Customer
from models.user import User

Base = declarative_base()

class Flat(Base):
    __tablename__ = 'tbl_cust_flat'

    flat_id = Column("pk_flat_id", Integer, primary_key=True, autoincrement=True)
    flat_no = Column(String(20), nullable=False)
    customer_id = Column("fk_cust_id", Integer, ForeignKey('tbl_customer.pk_cust_id'))
    society_id = Column("fk_soc_id", Integer, ForeignKey('tbl_society.pk_soc_id'))
    user_id = Column("fk_user_id", Integer, ForeignKey('tbl_users.id'))
    is_active = Column(String(10), nullable=False, default='Y')

    # Relationships
    customer = relationship('Customer', backref='flats')
    society = relationship('Society', backref='flats')
    user = relationship('User', backref='flats')

    def __repr__(self):
        return f"<CustFlat(pk_flat_id={self.pk_flat_id}, flat_no={self.flat_no})>"
