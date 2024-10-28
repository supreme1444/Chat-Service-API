import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, DateTime
from sqlalchemy.orm import relationship

from database import Base

metadata = MetaData()
class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,index=True,nullable=True)
    password = Column(String,nullable = True)
    telegram_id = Column(String,unique=True,nullable=True)

class MessageUser(Base):
    __tablename__ = "messages"

    id = Column(Integer,primary_key=True,index=True)
    sender_id = Column(Integer,ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    message = Column(String)
    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])
    datetime = Column(DateTime, default=datetime.datetime.utcnow)