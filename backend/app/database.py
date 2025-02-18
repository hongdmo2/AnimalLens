"""
Database Management Module

This module handles all database operations for the Animal Lens application.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text
from fastapi import HTTPException  # ✅ FastAPI exception handling added
from .config import settings
from .models import Animal, AnalysisResult
from typing import List, Dict
from contextlib import asynccontextmanager
from .logger import logger
import ssl

# create SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

engine = create_async_engine(
    settings.DATABASE_URL.replace('postgresql', 'postgresql+asyncpg'),
    echo=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    #connect_args={"ssl": ssl_context}
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
# Database class
class Database:
    def __init__(self):
        self.session_maker = AsyncSessionLocal

    # Transaction context manager   
    @asynccontextmanager
    async def transaction(self):
        """Transaction context manager for database operations"""
        async with self.session_maker() as session:
            async with session.begin():
                yield session

    # Check if the given label matches a known animal.
    async def is_animal(self, label: str) -> bool:
        """
        Check if the given label matches a known animal.
        """
        async with self.session_maker() as session:
            query = select(Animal).filter(
                Animal.name.ilike(f"%{label}%") | Animal.species.ilike(f"%{label}%")
            )
            result = await session.execute(query)
            is_match = bool(result.scalar_one_or_none())
            logger.debug(f"Checking if '{label}' is known animal. Query result: {is_match}")
            return is_match

    # Save analysis result to database.
    async def save_analysis_result(self, image_url: str, label: str, confidence: float) -> AnalysisResult:
        """
        Save analysis result to database.
        """
        async with self.session_maker() as session:
            query = select(Animal).filter(Animal.name.ilike(f"%{label}%"))
            result = await session.execute(query)
            animal = result.scalar_one_or_none()

            analysis_result = AnalysisResult(
                image_url=image_url,
                label=label,
                confidence=confidence,
                matched_animal_id=animal.id if animal else None
            )
            session.add(analysis_result)
            await session.commit()
            await session.refresh(analysis_result)
            return analysis_result

    # Save unidentified animal data.
    async def save_unidentified_animal(self, image_url: str, label: str, confidence: float) -> Dict:
        """
        Save unidentified animal data.
        """
        logger.info(f"Attempting to save unidentified animal: label={label}, confidence={confidence}, image_url={image_url}")

        async with self.session_maker() as session:
            try:

                query_unidentified = text("""
                    INSERT INTO unidentified_animals (
                        label,
                        confidence,
                        image_url
                    )
                    VALUES (
                        :label,
                        :confidence,
                        :image_url
                    )
                        RETURNING id
                    """)

                result = await session.execute(query_unidentified, {
                "label": label,
                "confidence": confidence,
                "image_url": image_url
                })
                await session.commit()
                unidentified_id = result.scalar()

                if not unidentified_id:
                    logger.error("Failed to insert into `unidentified_animals`")
                    raise HTTPException(status_code=500, detail="Failed to insert unidentified animal")

                logger.info(f"Unidentified animal inserted with ID: {unidentified_id}")




                query_analysis = text("""
                    INSERT INTO analysis_results (
                        image_url,
                        label,
                        confidence,
                        created_at
                    )
                    VALUES (
                        :image_url,
                        :label,
                        :confidence,
                        now()
                    )
                    RETURNING id
                """)
                result_analysis = await session.execute(query_analysis, {
                    "image_url": image_url,
                    "label": label,
                    "confidence": confidence
                })
                await session.commit()
                analysis_id = result_analysis.scalar()

                logger.info(f"Analysis result inserted with ID: {analysis_id}")

                return {
                    "unidentified_id": unidentified_id,
                    "analysis_id": analysis_id,
                    "image_url": image_url,
                    "label": label,
                    "confidence": confidence,
                    "message": "We are processing your image. Our team will review it soon."
                }

            except Exception as e:
                await session.rollback()
                logger.error(f"Error while saving unidentified animal: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail="Database error while saving unidentified animal")

    # Retrieve unidentified animal data by ID.
    async def get_unidentified_animal(self, result_id: str) -> Dict:
        """
        Retrieve unidentified animal data by ID.
        """
        async with self.session_maker() as session:
            try:
                numeric_id = int(result_id)
                logger.info(f"Fetching animal with ID: {numeric_id}")
                query = text("""
                    SELECT 
                        id,
                        label,
                        confidence,
                        image_url
                    FROM unidentified_animals
                    WHERE id = :id
                """)
                result = await session.execute(query, {"id": numeric_id})
                row = result.first()

                
                if row is None:
                    logger.error(f"Unidentified animal with ID {result_id} not found in database")
                    raise HTTPException(status_code=404, detail="Unidentified animal not found")
                
                logger.info(f"Retrieved row: {row}")

                return {
                    "id": str(row.id),
                    "image_url": row.image_url,
                    "label": row.label,
                    "confidence": row.confidence,
                    "message": "We don't have enough data about this animal yet. Our team will review and add it to our database soon."
                }
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid ID format")
# Database instance
database = Database()  
