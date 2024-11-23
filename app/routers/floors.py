from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Floor])
def get_floors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    floors = db.query(models.Floor).offset(skip).limit(limit).all()
    return floors

@router.post("/", response_model=schemas.Floor)
def create_floor(floor: schemas.FloorCreate, db: Session = Depends(get_db)):
    db_floor = models.Floor(**floor.dict())
    db.add(db_floor)
    db.commit()
    db.refresh(db_floor)
    return db_floor

@router.get("/{floor_id}", response_model=schemas.Floor)
def get_floor(floor_id: int, db: Session = Depends(get_db)):
    floor = db.query(models.Floor).filter(models.Floor.floor_id == floor_id).first()
    if floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    return floor

@router.put("/{floor_id}", response_model=schemas.Floor)
def update_floor(floor_id: int, floor: schemas.FloorCreate, db: Session = Depends(get_db)):
    db_floor = db.query(models.Floor).filter(models.Floor.floor_id == floor_id).first()
    if db_floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    
    for key, value in floor.dict().items():
        setattr(db_floor, key, value)
    
    db.commit()
    db.refresh(db_floor)
    return db_floor

@router.delete("/{floor_id}", response_model=schemas.Floor)
def delete_floor(floor_id: int, db: Session = Depends(get_db)):
    db_floor = db.query(models.Floor).filter(models.Floor.floor_id == floor_id).first()
    if db_floor is None:
        raise HTTPException(status_code=404, detail="Floor not found")
    
    db.delete(db_floor)
    db.commit()
    return db_floor
