from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Float, ARRAY, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

Base = declarative_base()

class Species(Base):
  __tablename__ = "species"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  common_name: Mapped[String] = mapped_column(String)
  scientific_name: Mapped[String] = mapped_column(String)

  bird_songs: Mapped[List["BirdSong"]] = relationship(back_populates="species")

class BirdSong(Base):
  __tablename__ = "bird_song"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  filename: Mapped[str] = mapped_column(String)
  vector: Mapped[List[Float]] = mapped_column(ARRAY(Float))
  species_id: Mapped[int] = mapped_column(ForeignKey("species.id"))

  species: Mapped["Species"] = relationship(back_populates="bird_songs")