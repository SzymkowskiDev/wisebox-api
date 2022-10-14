from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base  = declarative_base()

class Item(Base):
    __tablename__ = 'item'
    id  = Column(Integer, primary_key=True, index=True)
    product = Column(String)
    quantity = Column(Integer)
    price = Column(Float)
    location = Column(String)
    status = Column(String)
    magazine_id = Column(Integer, ForeignKey('magazine.id'))
    # time_created = Column(DateTime(timezone=True), server_default=func.now())
    # time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    magazine = relationship('Magazine')


class Magazine(Base):
    __tablename__ = 'magazine'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    avatar = Column(String)
    location = Column(String)

    # time_created = Column(DateTime(timezone=True), server_default=func.now())
    # time_updated = Column(DateTime(timezone=True), onupdate=func.now())

