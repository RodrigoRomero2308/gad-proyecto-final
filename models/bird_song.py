from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

Base = declarative_base()

class BirdSong(Base):
  __tablename__ = "bird_song"

  id = Column(Integer, primary_key=True, autoincrement=True)
  filename = Column(String)
  vector = Column(ARRAY(Float))
  species_id = Column(Integer, ForeignKey("species.id"))

  species = relationship("Species", back_populates="bird_songs")