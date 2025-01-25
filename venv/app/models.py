from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# SQLite database connection
engine = create_engine('sqlite:///test.db', echo=True)

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Integer)

engine = create_engine('sqlite:///analytics.db')

#Create Tables
Base.metadata.create_all(engine)
