from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Bed])
def get_beds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    beds = db.query(models.Bed).offset(skip).limit(limit).all()
    return beds

@router.post("/", response_model=schemas.Bed)
def create_bed(bed: schemas.BedCreate, db: Session = Depends(get_db)):
    db_bed = models.Bed(**bed.dict())
    db.add(db_bed)
    db.commit()
    db.refresh(db_bed)
    return db_bed

@router.get("/{bed_id}", response_model=schemas.Bed)
def get_bed(bed_id: int, db: Session = Depends(get_db)):
    bed = db.query(models.Bed).filter(models.Bed.bed_id == bed_id).first()
    if bed is None:
        raise HTTPException(status_code=404, detail="Bed not found")
    return bed

@router.put("/{bed_id}", response_model=schemas.Bed)
def update_bed(bed_id: int, bed: schemas.BedCreate, db: Session = Depends(get_db)):
    db_bed = db.query(models.Bed).filter(models.Bed.bed_id == bed_id).first()
    if db_bed is None:
        raise HTTPException(status_code=404, detail="Bed not found")
    
    for key, value in bed.dict().items():
        setattr(db_bed, key, value)
    
    db.commit()
    db.refresh(db_bed)
    return db_bed

@router.delete("/{bed_id}", response_model=schemas.Bed)
def delete_bed(bed_id: int, db: Session = Depends(get_db)):
    db_bed = db.query(models.Bed).filter(models.Bed.bed_id == bed_id).first()
    if db_bed is None:
        raise HTTPException(status_code=404, detail="Bed not found")
    
    db.delete(db_bed)
    db.commit()
    return db_bed
