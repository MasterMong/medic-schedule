from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from .. import models
from ..database import get_db, Base, engine
from ..seeders.seeder import seed_data  # Add this import

router = APIRouter()

@router.get("/clear", response_model=Dict[str, str])
async def clear_database(confirmation: bool = False, db: Session = Depends(get_db)):
    if not confirmation:
        raise HTTPException(status_code=400, detail="Confirmation required to clear database")
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    # Recreate all tables
    Base.metadata.create_all(bind=engine)
    
    return {"message": "Database cleared successfully"}

@router.get("/seed", response_model=Dict[str, str])
async def seed_database(db: Session = Depends(get_db)):
    try:
        seed_data(db)
        return {"message": "Database seeded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))