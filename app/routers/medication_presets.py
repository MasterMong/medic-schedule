from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.MedicationPreset])
def get_medication_presets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    presets = db.query(models.MedicationPreset).offset(skip).limit(limit).all()
    return presets

@router.post("/", response_model=schemas.MedicationPreset)
def create_medication_preset(preset: schemas.MedicationPresetCreate, db: Session = Depends(get_db)):
    db_preset = models.MedicationPreset(**preset.dict())
    db.add(db_preset)
    db.commit()
    db.refresh(db_preset)
    return db_preset

@router.get("/{preset_id}", response_model=schemas.MedicationPreset)
def get_medication_preset(preset_id: int, db: Session = Depends(get_db)):
    preset = db.query(models.MedicationPreset).filter(models.MedicationPreset.preset_id == preset_id).first()
    if preset is None:
        raise HTTPException(status_code=404, detail="Medication preset not found")
    return preset

@router.put("/{preset_id}", response_model=schemas.MedicationPreset)
def update_medication_preset(preset_id: int, preset: schemas.MedicationPresetCreate, db: Session = Depends(get_db)):
    db_preset = db.query(models.MedicationPreset).filter(models.MedicationPreset.preset_id == preset_id).first()
    if db_preset is None:
        raise HTTPException(status_code=404, detail="Medication preset not found")
    
    for key, value in preset.dict().items():
        setattr(db_preset, key, value)
    
    db.commit()
    db.refresh(db_preset)
    return db_preset

@router.delete("/{preset_id}", response_model=schemas.MedicationPreset)
def delete_medication_preset(preset_id: int, db: Session = Depends(get_db)):
    db_preset = db.query(models.MedicationPreset).filter(models.MedicationPreset.preset_id == preset_id).first()
    if db_preset is None:
        raise HTTPException(status_code=404, detail="Medication preset not found")
    
    db.delete(db_preset)
    db.commit()
    return db_preset