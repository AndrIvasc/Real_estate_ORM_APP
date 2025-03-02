from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Base class for all ORM models
Base = declarative_base()

# Creating an SQLite database and a session factory
engine = create_engine("sqlite:///real_estate.db")
Session = sessionmaker(bind=engine)
session = Session()


# Models
class Owner(Base):
    """
    Represents a property owner.
    """
    __tablename__ = "owners"
    owner_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, unique=True)


class City(Base):
    """
    Represents a city where properties are located.
    """
    __tablename__ = "cities"
    city_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Address(Base):
    """
    Represents a physical address associated with a property.
    """
    __tablename__ = "addresses"
    address_id = Column(Integer, primary_key=True)
    street_address = Column(String)
    postal_code = Column(String)
    city_id = Column(Integer, ForeignKey("cities.city_id"))
    city = relationship("City")


class Property(Base):
    """
    Represents a real estate property.
    """
    __tablename__ = "properties"
    property_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("owners.owner_id"))
    address_id = Column(Integer, ForeignKey("addresses.address_id"))
    area_sqm = Column(Float)
    registry_number = Column(String, unique=True)
    address = relationship("Address")
    owner = relationship("Owner")


class Agency(Base):
    """
    Represents a real estate agency managing property listings.
    """
    __tablename__ = "agencies"
    agency_id = Column(Integer, primary_key=True)
    name = Column(String)
    company_code = Column(String, unique=True)


class Listing(Base):
    """
    Represents a property listing for sale or rent.
    """
    __tablename__ = "listings"
    listing_id = Column(Integer, primary_key=True)
    property_id = Column(Integer, ForeignKey("properties.property_id"))
    agency_id = Column(Integer, ForeignKey("agencies.agency_id"))
    sale_price = Column(Float)
    rental_price = Column(Float)
    property = relationship("Property")
    agency = relationship("Agency")


def initialize_database():
    """
    Initializes the database by creating all defined tables.
    """
    Base.metadata.create_all(engine)
    print("Database initialized.")
