from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Animal model
class Animal(Base):
    __tablename__ = "animals"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    species = Column(String(100))
    habitat = Column(String)
    diet = Column(String)
    description = Column(String)

# AnalysisResult model
class AnalysisResult(Base):
    __tablename__ = "analysis_results"
    
    id = Column(Integer, primary_key=True)
    image_url = Column(String, nullable=False)
    label = Column(String(100))
    confidence = Column(Float)
    matched_animal_id = Column(Integer, ForeignKey("animals.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    matched_animal = relationship("Animal", backref="analysis_results") 