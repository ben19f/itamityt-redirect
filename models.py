from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    items = relationship("Item", back_populates="user")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    link_id = Column(String(50), unique=True, index=True, nullable=False)

    owner_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="items")

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    clicks = relationship("Click", back_populates="item")  # связь с кликами

class Click(Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(String(50), ForeignKey("items.link_id"))  # теперь FK на items
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    ip = Column(String(50))
    user_agent = Column(Text)

    item = relationship("Item", back_populates="clicks")