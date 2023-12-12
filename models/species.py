from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

Base = declarative_base()

class Species(Base):
  __tablename__ = "species"

  id = Column(Integer, primary_key=True, autoincrement=True)
  common_name = Column(String)
  scientific_name = Column(String)

  bird_songs = relationship("BirdSong", back_populates="species")