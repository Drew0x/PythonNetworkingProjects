'''
CS 3700 - Networking & Distributed Computing - Fall 2025
Instructor: Thyago Mota
Student(s): Andrew Stephens
Description: Project 02 - Incidents WS (models)
'''

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Key(Base):
    __tablename__ = 'keys'
    key = Column(String(32), primary_key=True)

# TODO #2: complete the definition of the Incident's model class
class Incident(Base):
    __tablename__ = 'incidents'

    slug = Column(String(16), primary_key = True)
    event_date = Column(Date, nullable = False)
    year = Column(Integer, nullable = False)
    month = Column(Integer, nullable = False)
    actor = Column(String(50), nullable = False)
    actor_type = Column(String(25), nullable = False)
    organization = Column(String(100), nullable = False)
    industry_code = Column(Integer, nullable = False)
    industry = Column(String(100), nullable = False)
    motive = Column(String(50), nullable = False)
    event_type = Column(String(50), nullable = False)
    event_subtype = Column(String(50), nullable = False)
    description = Column(String(250), nullable = False)
    source_url = Column(String(200), nullable = False)
    country = Column(String(100), nullable = False)
    actor_country = Column(String(100), nullable = False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
             
        
