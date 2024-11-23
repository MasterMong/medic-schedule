from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Nurse])
def get_nurses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    nurses = db.query(models.Nurse).offset(skip).limit(limit).all()
    return nurses

@router.post("/", response_model=schemas.Nurse)
def create_nurse(nurse: schemas.NurseCreate, db: Session = Depends(get_db)):
    db_nurse = models.Nurse(**nurse.dict())
    db.add(db_nurse)
    db.commit()
    db.refresh(db_nurse)
    return db_nurse

@router.get("/{nurse_id}", response_model=schemas.Nurse)
def get_nurse(nurse_id: int, db: Session = Depends(get_db)):
    nurse = db.query(models.Nurse).filter(models.Nurse.nurse_id == nurse_id).first()
    if nurse is None:
        raise HTTPException(status_code=404, detail="Nurse not found")
    return nurse

@router.put("/{nurse_id}", response_model=schemas.Nurse)
def update_nurse(nurse_id: int, nurse: schemas.NurseCreate, db: Session = Depends(get_db)):
    db_nurse = db.query(models.Nurse).filter(models.Nurse.nurse_id == nurse_id).first()
    if db_nurse is None:
        raise HTTPException(status_code=404, detail="Nurse not found")
    
    for key, value in nurse.dict().items():
        setattr(db_nurse, key, value)
    
    db.commit()
    db.refresh(db_nurse)
    return db_nurse

@router.delete("/{nurse_id}", response_model=schemas.Nurse)
def delete_nurse(nurse_id: int, db: Session = Depends(get_db)):
    db_nurse = db.query(models.Nurse).filter(models.Nurse.nurse_id == nurse_id).first()
    if db_nurse is None:
        raise HTTPException(status_code=404, detail="Nurse not found")
    
    db.delete(db_nurse)
    db.commit()
    return db_nurse
