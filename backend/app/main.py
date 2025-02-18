from fastapi import FastAPI, UploadFile, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from .database import database, AsyncSessionLocal
from sqlalchemy.orm import joinedload
from .config import settings
from .logger import logger  # 이것만 사용
from PIL import Image
import io
from sqlalchemy import text, select
from .models import AnalysisResult

"""
FastAPI Main Application File
Roles:
1. Define API endpoints (/api/upload, /api/results/{id}, etc.)
2. Coordinate image upload and analysis processes
3. Handle error processing and API responses
4. Configure CORS and other middleware
"""
app = FastAPI(
    title="Animal Lens API",
    description="Animal detection and identification API"
)

# CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
from .services.s3_service import s3_service
from .services import rekognition_service

@app.get("/")
async def root():
    """
    Root route handler - Check if the API is running
    """
    return {
        "status": "ok",
        "message": "Animal Lens API is running"
    }

@app.post("/api/upload")
async def upload_image(file: UploadFile):
    """
    Image upload and analysis endpoint
    """
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Only image files are allowed")
        
        # Validate file size (5MB limit)
        contents = await file.read()
        if len(contents) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size must be less than 5MB")
        
        logger.info(f"Processing upload: {file.filename}, size: {len(contents)}")
        
        # Upload to S3
        image_url = await s3_service.upload_file(contents, file.filename)
        logger.info(f"Uploaded to S3: {image_url}")
        
        # Rekognition analysis
        labels = await rekognition_service.detect_labels(image_url)
        logger.info(f"Rekognition labels: {labels}")
        
        # Process results
        result = await process_analysis_results(image_url, labels)
        return result
        
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close()

async def process_analysis_results(image_url: str, labels: list) -> dict:
    """Process and save analysis results"""
    logger.info("=== Starting analysis results processing ===")
    logger.debug(f"Image URL: {image_url}")
    logger.debug(f"All labels: {labels}")
    
    # Exclude generic labels
    GENERIC_LABELS = {
        'Animal', 'Mammal', 'Wildlife', 'Pet', 'Fauna',
        'Canine',  # Additional: more general classification
        'Carnivore',
        'Feline','Face'
    }
    
    # Label priority (more specific order)
    PRIORITY_LABELS = [
        'Golden Retriever', 'Labrador', 'Poodle',  # More specific breeds
        'Dog',  # General species
        'Puppy'  # 기타
    ]
    
    # Filter high confidence labels
    high_confidence_labels = [
        label for label in labels 
        if label["confidence"] >= 80 and 
        label["name"] not in GENERIC_LABELS
    ]
    logger.info(f"Filtered specific animal labels: {high_confidence_labels}")
    
    if not high_confidence_labels:
        logger.warning("No specific animals detected in image")
        raise HTTPException(400, "No specific animals detected in image")
    
    # Select label based on priority
    selected_label = None
    for priority_name in PRIORITY_LABELS:
        matching_labels = [
            label for label in high_confidence_labels 
            if label["name"] == priority_name
        ]
        if matching_labels:
            selected_label = max(matching_labels, key=lambda x: x["confidence"])
            break
    
    # If no priority label, select the highest confidence label
    if not selected_label:
        selected_label = max(high_confidence_labels, key=lambda x: x["confidence"])
    
    logger.info(f"Selected specific animal: {selected_label}")
    
    # Check if animal is known in the database
    is_known_animal = await database.is_animal(selected_label["name"])
    logger.info(f"Database lookup - Animal '{selected_label['name']}' is known: {is_known_animal}")
    
    if not is_known_animal:
        logger.debug("Processing unknown animal")
        try:
            result = await database.save_unidentified_animal(
                image_url=image_url,
                label=selected_label["name"],
                confidence=selected_label["confidence"]
            )
            logger.info(f"Successfully saved unidentified animal: {result}")  #log
            return result
        except Exception as e:
            logger.error(f"Failed to save unidentified animal: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Database save failed")  #exception

    if is_known_animal:
        logger.debug("Processing known animal")
        result = await database.save_analysis_result(
            image_url=image_url,
            label=selected_label["name"],
            confidence=selected_label["confidence"]
        )
        return {
            # Same as Unknown Animal, use 'analysis_id' key
            "analysis_id": str(result.id),
            "image_url": image_url,
            "label": selected_label["name"],
            "confidence": selected_label["confidence"],
            "message": "We are processing your image. Our team will review it soon."
            # If needed, add/remove fields similar to the "message" field in Unknown Animal
        }
    else:
        logger.debug("Processing unknown animal")
        # save_unidentified_animal() function already returns {"analysis_id": ..., "image_url":..., "label":..., "confidence":...}
        # So, use the same structure
        
        return await database.save_unidentified_animal(
            image_url=image_url,
            label=selected_label["name"],
            confidence=selected_label["confidence"]
        )

@app.get("/api/test")
async def test_connection():
    return {"status": "ok", "message": "Backend is running"}

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/api/results/{result_id}")
async def get_analysis_result(result_id: int, db: AsyncSession = Depends(get_db)):
    # 1) Query AnalysisResult while joinedload matched_animal
    query = (
        select(AnalysisResult)
        .options(joinedload(AnalysisResult.matched_animal))  
        .where(AnalysisResult.id == result_id)
    )

    # 2) Execute query and get one AnalysisResult object
    result = await db.execute(query)
    analysis = result.scalar_one_or_none()

    if not analysis:
        raise HTTPException(status_code=404, detail="Result not found")

    # 3) Create matched_animal data
    matched_animal_data = None
    if analysis.matched_animal:
        matched_animal_data = {
            "id": analysis.matched_animal.id,
            "name": analysis.matched_animal.name,
            "species": analysis.matched_animal.species,
            "habitat": analysis.matched_animal.habitat,
            "diet": analysis.matched_animal.diet,
            "description": analysis.matched_animal.description
        }

    # 4) Configure JSON response
    return {
        "id": analysis.id,
        "image_url": analysis.image_url,
        "label": analysis.label,
        "confidence": analysis.confidence,
        "created_at": analysis.created_at,
        # Include Animal information
        "matched_animal": matched_animal_data
    }

@app.get("/api/db-test")
async def test_db_connection():
    """Test database connection"""
    try:
        async with database.transaction() as session:
            # Execute the simplest query
            result = await session.execute(text("SELECT 1"))
            # Process result without await and directly call scalar()
            value = result.scalar()
            logger.debug(f"Database test result: {value}")
            return {"status": "ok", "message": "Database connection successful"}
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise HTTPException(500, f"Database connection failed: {str(e)}")

