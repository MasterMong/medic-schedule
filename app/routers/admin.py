
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict
from .. import models
from ..database import get_db

router = APIRouter()

@router.post("/clear-database", response_model=Dict[str, str])
async def clear_database(confirmation: bool = False, db: Session = Depends(get_db)):
    if not confirmation:
        raise HTTPException(status_code=400, detail="Confirmation required to clear database")
    
    # Clear tables in order (respecting foreign keys)
    db.query(models.MedicationHistory).delete()
    db.query(models.MedicationSchedule).delete()
    db.query(models.Patient).delete()
    db.query(models.Medication).delete()
    db.query(models.MedicationPreset).delete()
    db.query(models.Nurse).delete()
    db.query(models.Bed).delete()
    db.query(models.Room).delete()
    db.query(models.Floor).delete()
    db.query(models.Ward).delete()
    db.query(models.Building).delete()
    
    db.commit()
    
    return {"message": "Database cleared successfully"}