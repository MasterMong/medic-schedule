from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from .. import models
from ..database import get_db, Base, engine

router = APIRouter()

@router.post("/clear-database", response_model=Dict[str, str])
async def clear_database(confirmation: bool = False, db: Session = Depends(get_db)):
    if not confirmation:
        raise HTTPException(status_code=400, detail="Confirmation required to clear database")
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    # Recreate all tables
    Base.metadata.create_all(bind=engine)
    
    return {"message": "Database cleared successfully"}