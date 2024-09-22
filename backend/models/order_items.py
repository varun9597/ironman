from sqlalchemy import Column, Integer, ForeignKey, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.item import Item
from models.order import Order

Base = declarative_base()

class OrderItem(Base):
    __tablename__ = 'tbl_order_items'

    order_item_id = Column("pk_order_item_id", Integer, primary_key=True, autoincrement=True)
    order_id = Column("fk_order_id", Integer, ForeignKey('tbl_orders.pk_order_id'), nullable=True)
    item_id = Column("fk_item_id", Integer, ForeignKey('tbl_items.pk_item_id'), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    price = Column(Numeric(10, 2), nullable=False, default=0.00)
    is_active = Column(String(10), nullable=False, default='Y')

    # Relationships
    order = relationship('Order', backref='order_items')
    item = relationship('Item', backref='order_items')

    def __repr__(self):
        return f"<OrderItem(pk_order_item_id={self.pk_order_item_id}, quantity={self.quantity}, price={self.price})>"
