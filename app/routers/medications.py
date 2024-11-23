from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Medication])
def get_medications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    medications = db.query(models.Medication).offset(skip).limit(limit).all()
    return medications

@router.post("/", response_model=schemas.Medication)
def create_medication(medication: schemas.MedicationCreate, db: Session = Depends(get_db)):
    db_medication = models.Medication(**medication.dict())
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication

@router.get("/{medication_id}", response_model=schemas.Medication)
def get_medication(medication_id: int, db: Session = Depends(get_db)):
    medication = db.query(models.Medication).filter(models.Medication.medication_id == medication_id).first()
    if medication is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication

@router.put("/{medication_id}", response_model=schemas.Medication)
def update_medication(medication_id: int, medication: schemas.MedicationCreate, db: Session = Depends(get_db)):
    db_medication = db.query(models.Medication).filter(models.Medication.medication_id == medication_id).first()
    if db_medication is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    
    for key, value in medication.dict().items():
        setattr(db_medication, key, value)
    
    db.commit()
    db.refresh(db_medication)
    return db_medication

@router.delete("/{medication_id}")
def delete_medication(medication_id: int, db: Session = Depends(get_db)):
    db_medication = db.query(models.Medication).filter(models.Medication.medication_id == medication_id).first()
    if db_medication is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    
    db.delete(db_medication)
    db.commit()
    return {"message": "Medication deleted successfully"}
