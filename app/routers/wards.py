from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Ward])
def get_wards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    wards = db.query(models.Ward).offset(skip).limit(limit).all()
    return wards

@router.post("/", response_model=schemas.Ward)
def create_ward(ward: schemas.WardCreate, db: Session = Depends(get_db)):
    db_ward = models.Ward(**ward.dict())
    db.add(db_ward)
    db.commit()
    db.refresh(db_ward)
    return db_ward

@router.get("/{ward_id}", response_model=schemas.Ward)
def get_ward(ward_id: int, db: Session = Depends(get_db)):
    ward = db.query(models.Ward).filter(models.Ward.ward_id == ward_id).first()
    if ward is None:
        raise HTTPException(status_code=404, detail="Ward not found")
    return ward

@router.put("/{ward_id}", response_model=schemas.Ward)
def update_ward(ward_id: int, ward: schemas.WardCreate, db: Session = Depends(get_db)):
    db_ward = db.query(models.Ward).filter(models.Ward.ward_id == ward_id).first()
    if db_ward is None:
        raise HTTPException(status_code=404, detail="Ward not found")
    
    for key, value in ward.dict().items():
        setattr(db_ward, key, value)
    
    db.commit()
    db.refresh(db_ward)
    return db_ward

@router.delete("/{ward_id}", response_model=schemas.Ward)
def delete_ward(ward_id: int, db: Session = Depends(get_db)):
    db_ward = db.query(models.Ward).filter(models.Ward.ward_id == ward_id).first()
    if db_ward is None:
        raise HTTPException(status_code=404, detail="Ward not found")
    
    db.delete(db_ward)
    db.commit()
    return db_ward
