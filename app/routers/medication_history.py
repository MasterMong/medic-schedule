
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.MedicationHistory])
def get_medication_histories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    histories = db.query(models.MedicationHistory).offset(skip).limit(limit).all()
    return histories

@router.post("/", response_model=schemas.MedicationHistory)
def create_medication_history(history: schemas.MedicationHistoryCreate, db: Session = Depends(get_db)):
    db_history = models.MedicationHistory(**history.dict())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

@router.get("/{history_id}", response_model=schemas.MedicationHistory)
def get_medication_history(history_id: int, db: Session = Depends(get_db)):
    history = db.query(models.MedicationHistory).filter(models.MedicationHistory.history_id == history_id).first()
    if history is None:
        raise HTTPException(status_code=404, detail="Medication history not found")
    return history

@router.put("/{history_id}", response_model=schemas.MedicationHistory)
def update_medication_history(history_id: int, history: schemas.MedicationHistoryCreate, db: Session = Depends(get_db)):
    db_history = db.query(models.MedicationHistory).filter(models.MedicationHistory.history_id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="Medication history not found")
    
    for key, value in history.dict().items():
        setattr(db_history, key, value)
    
    db.commit()
    db.refresh(db_history)
    return db_history

@router.delete("/{history_id}", response_model=schemas.MedicationHistory)
def delete_medication_history(history_id: int, db: Session = Depends(get_db)):
    db_history = db.query(models.MedicationHistory).filter(models.MedicationHistory.history_id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="Medication history not found")
    
    db.delete(db_history)
    db.commit()
    return db_history