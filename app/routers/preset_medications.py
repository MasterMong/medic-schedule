
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.PresetMedication])
def get_preset_medications(
    skip: int = 0, 
    limit: int = 100, 
    preset_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.PresetMedication)
    if preset_id:
        query = query.filter(models.PresetMedication.preset_id == preset_id)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.PresetMedication)
def create_preset_medication(
    preset_medication: schemas.PresetMedicationCreate, 
    db: Session = Depends(get_db)
):
    db_preset_medication = models.PresetMedication(**preset_medication.dict())
    db.add(db_preset_medication)
    db.commit()
    db.refresh(db_preset_medication)
    return db_preset_medication

@router.get("/{preset_med_id}", response_model=schemas.PresetMedication)
def get_preset_medication(preset_med_id: int, db: Session = Depends(get_db)):
    preset_medication = db.query(models.PresetMedication).filter(
        models.PresetMedication.preset_med_id == preset_med_id
    ).first()
    if preset_medication is None:
        raise HTTPException(status_code=404, detail="Preset medication not found")
    return preset_medication

@router.put("/{preset_med_id}", response_model=schemas.PresetMedication)
def update_preset_medication(
    preset_med_id: int, 
    preset_medication: schemas.PresetMedicationCreate, 
    db: Session = Depends(get_db)
):
    db_preset_medication = db.query(models.PresetMedication).filter(
        models.PresetMedication.preset_med_id == preset_med_id
    ).first()
    if db_preset_medication is None:
        raise HTTPException(status_code=404, detail="Preset medication not found")
    
    for key, value in preset_medication.dict().items():
        setattr(db_preset_medication, key, value)
    
    db.commit()
    db.refresh(db_preset_medication)
    return db_preset_medication

@router.delete("/{preset_med_id}", response_model=schemas.PresetMedication)
def delete_preset_medication(preset_med_id: int, db: Session = Depends(get_db)):
    db_preset_medication = db.query(models.PresetMedication).filter(
        models.PresetMedication.preset_med_id == preset_med_id
    ).first()
    if db_preset_medication is None:
        raise HTTPException(status_code=404, detail="Preset medication not found")
    
    db.delete(db_preset_medication)
    db.commit()
    return db_preset_medication