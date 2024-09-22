from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.customer import Customer
from models.user import User

Base = declarative_base()

class Order(Base):
    __tablename__ = 'tbl_orders'

    order_id = Column("pk_order_id", Integer, primary_key=True, autoincrement=True)
    customer_id = Column("fk_cust_id", Integer, ForeignKey('tbl_customer.pk_cust_id'), nullable=False)
    user_id = Column("fk_user_id", Integer, ForeignKey('tbl_users.id'), nullable=False)
    order_date = Column(TIMESTAMP, nullable=False, default='CURRENT_TIMESTAMP')
    total_amt = Column(Numeric(10, 2), nullable=False, default=0.00)
    paid_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    os_amount = Column(Numeric(10, 2), nullable=False, default=0.00)
    bill_status = Column(String(20), nullable=False, default='Not Paid')
    is_active = Column(String(10), nullable=False, default='Y')

    # Relationships
    customer = relationship('Customer', backref='orders')
    user = relationship('User', backref='orders')

    def __repr__(self):
        return f"<Order(pk_order_id={self.pk_order_id}, total_amt={self.total_amt})>"
