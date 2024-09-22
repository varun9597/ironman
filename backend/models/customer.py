from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.society import Society
from models.user import User

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'tbl_customer'

    customer_id = Column("pk_cust_id", Integer, primary_key=True, autoincrement=True)
    customer_guid = Column("cust_id", String(155), nullable=False, default="uuid()")  # Generate UUID-like string
    customer_name = Column("cust_name", String(255), nullable=False)
    society_id = Column("fk_soc_id", Integer, ForeignKey('tbl_society.pk_soc_id'))
    customer_phone = Column(String(15), nullable=False)
    user_id = Column("fk_user_id", Integer, ForeignKey('tbl_users.id'))
    is_active = Column(String(10), nullable=False, default='Y')

    # Relationships
    society = relationship('Society', backref='customers')
    user = relationship('User', backref='customers')

    def __repr__(self):
        return f"<Customer(pk_cust_id={self.pk_cust_id}, cust_name={self.cust_name})>"
