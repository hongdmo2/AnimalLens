"""
Database Management Module

This module handles all database operations for the Animal Lens application.
It provides functionality for managing animal data and analysis results.

Features:
1. Database connection and session management
2. Animal data querying and storage
3. Analysis results storage and retrieval
4. Unidentified animal data management
5. Asynchronous database operations
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text
from .config import settings
from .models import Animal, AnalysisResult
from typing import List, Dict
from contextlib import asynccontextmanager
from .logger import logger

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

class Database:
    def __init__(self):
        self.session_maker = AsyncSessionLocal
    
    @asynccontextmanager
    async def transaction(self):
        """Transaction context manager for database operations"""
        async with self.session_maker() as session:
            async with session.begin():
                yield session
    
    async def is_animal(self, label: str) -> bool:
        """
        Check if the given label matches a known animal.
        
        Args:
            label (str): The label to check
            
        Returns:
            bool: True if the label matches a known animal, False otherwise
        """
        async with self.session_maker() as session:
            # Case-insensitive partial match search
            query = select(Animal).filter(
                Animal.name.ilike(f"%{label}%") |  # Search by name
                Animal.species.ilike(f"%{label}%")  # Search by species
            )
            result = await session.execute(query)
            is_match = bool(result.scalar_one_or_none())
            logger.debug(f"Checking if '{label}' is known animal. Query result: {is_match}")
            return is_match
    
    async def save_analysis_result(
        self,
        image_url: str,
        label: str,
        confidence: float
    ) -> AnalysisResult:
        """
        Save analysis result to database.
        
        Args:
            image_url (str): URL of the analyzed image
            label (str): Detected label
            confidence (float): Confidence score
            
        Returns:
            AnalysisResult: Created analysis result object
        """
        async with self.session_maker() as session:
            # Find matching animal
            query = select(Animal).filter(Animal.name.ilike(f"%{label}%"))
            result = await session.execute(query)
            animal = result.scalar_one_or_none()
            
            # Save result
            result = AnalysisResult(
                image_url=image_url,
                label=label,
                confidence=confidence,
                matched_animal_id=animal.id if animal else None
            )
            session.add(result)
            await session.commit()
            await session.refresh(result)
            return result

    async def find_matching_animals(self, label: str, confidence: float) -> List[Dict]:
        """
        Find all animals matching the given label.
        
        Args:
            label (str): Label to match
            confidence (float): Confidence score
            
        Returns:
            List[Dict]: List of matching animals with their details
        """
        async with self.session_maker() as session:
            query = select(Animal).filter(Animal.name.ilike(f"%{label}%"))
            result = await session.execute(query)
            animals = result.scalars().all()
            
            return [
                {
                    "id": animal.id,
                    "name": animal.name,
                    "confidence": confidence,
                    "habitat": animal.habitat,
                    "diet": animal.diet,
                    "description": animal.description
                }
                for animal in animals
            ]

    async def get_analysis_result(self, result_id: str) -> Dict:
        """
        Retrieve analysis result by ID.
        
        Args:
            result_id (str): ID of the analysis result
            
        Returns:
            Dict: Analysis result with matched animal data if available
        """
        async with self.session_maker() as session:
            try:
                numeric_id = int(result_id)
                
                # Query result with matched animal data
                query = select(AnalysisResult, Animal).join(
                    Animal,
                    AnalysisResult.matched_animal_id == Animal.id,
                    isouter=True
                ).filter(AnalysisResult.id == numeric_id)
                
                result = await session.execute(query)
                row = result.first()
                
                if not row:
                    return None
                
                analysis_result, animal = row
                
                return {
                    "id": str(analysis_result.id),
                    "image_url": analysis_result.image_url,
                    "label": analysis_result.label,
                    "confidence": analysis_result.confidence,
                    "animal": {
                        "name": animal.name,
                        "species": animal.species,
                        "habitat": animal.habitat,
                        "diet": animal.diet,
                        "description": animal.description
                    } if animal else None
                }
            except ValueError:
                return None

    async def save_unidentified_animal(
        self,
        image_url: str,
        label: str,
        confidence: float
    ) -> Dict:
        """
        Save unidentified animal data.
        
        Args:
            image_url (str): URL of the image
            label (str): Detected label
            confidence (float): Confidence score
            
        Returns:
            Dict: Saved unidentified animal data
        """
        async with self.session_maker() as session:
            unidentified = {
                'label': label,
                'confidence': confidence,
                'image_url': image_url
            }
            
            query = text("""
                INSERT INTO unidentified_animals (label, confidence, image_url)
                VALUES (:label, :confidence, :image_url)
                RETURNING id
            """)
            result = await session.execute(query, unidentified)
            await session.commit()
            
            row = result.first()
            unidentified_id = str(row[0]) if row else None
            
            return {
                "upload_id": unidentified_id,
                "image_url": image_url,
                "label": label,
                "confidence": confidence,
                "message": "We don't have enough data about this animal yet. Our team will review and add it to our database soon."
            }

    async def get_unidentified_animal(self, result_id: str) -> Dict:
        """
        Retrieve unidentified animal data by ID.
        
        Args:
            result_id (str): ID of the unidentified animal record
            
        Returns:
            Dict: Unidentified animal data if found
        """
        async with self.session_maker() as session:
            try:
                numeric_id = int(result_id)
                query = text("""
                    SELECT id, label, confidence, image_url
                    FROM unidentified_animals
                    WHERE id = :id
                """)
                result = await session.execute(query, {"id": numeric_id})
                row = result.first()
                
                if not row:
                    return None
                    
                return {
                    "id": str(row.id),
                    "image_url": row.image_url,
                    "label": row.label,
                    "confidence": row.confidence,
                    "message": "We don't have enough data about this animal yet. Our team will review and add it to our database soon."
                }
            except ValueError:
                return None

database = Database()