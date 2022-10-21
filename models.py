from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class Users(Base):
    __tablename__ = "USERS"

    USER_ID = Column(Integer, primary_key = True, autoincrement = True) # TODO: Make it auto-generate with identity function
    FIRST_NAME = Column(String)
    LAST_NAME = Column(String)
    EMAIL = Column(String)
    HASH_PASSWORD = Column(String)

    # What follows is not an attribute but the establishment of one-to-many relationship
    magazines = relationship("Magazines", back_populates = "users")

class Magazines(Base):
    __tablename__ = "MAGAZINES"

    USER_ID = Column(Integer, ForeignKey("USERS.USER_ID"))
    MAG_ID = Column(Integer, primary_key = True, autoincrement = True) # TODO: Make it auto-generate with identity function
    NAME = Column(String)
    DESCRIPTION = Column(String)
    AVATAR = Column(String)
    LOCATION = Column(String)
    DATE_OF_CREATION = Column(String) # TODO: Change to date later on

    # What follows is not an attribute but the establishment of one-to-many relationship
    users = relationship("Users", back_populates = "magazines")
    products = relationship("Products", back_populates = "magazines")

class Products(Base):
    __tablename__ = "PRODUCTS"

    MAG_ID = Column(Integer, ForeignKey("MAGAZINES.MAG_ID"))
    PROD_ID = Column(Integer, primary_key = True, autoincrement = True) # TODO: Make it auto-generate with identity function
    NAME = Column(String)
    STATUS = Column(String) # TODO: Check constraint
    QUANTITY = Column(Integer)
    PRICE = Column(Integer) # TODO: replace that with float
    DESCRIPTION = Column(String)
    IMAGE = Column(String)
    LOCATION = Column(String)
    EXPIRY_DATE = Column(Integer) # TODO: replace that with date

    # What follows is not an attribute but the establishment of one-to-many relationship
    magazines = relationship("Magazines", back_populates = "products")




























# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#
#     items = relationship("Item", back_populates="owner")
#
#
# class Item(Base):
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#
#     owner = relationship("User", back_populates="items")
