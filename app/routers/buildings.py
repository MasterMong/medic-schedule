from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Building])
def get_buildings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    buildings = db.query(models.Building).offset(skip).limit(limit).all()
    return buildings

@router.post("/", response_model=schemas.Building)
def create_building(building: schemas.BuildingCreate, db: Session = Depends(get_db)):
    db_building = models.Building(**building.dict())
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building

@router.get("/{building_id}", response_model=schemas.Building)
def get_building(building_id: int, db: Session = Depends(get_db)):
    building = db.query(models.Building).filter(models.Building.building_id == building_id).first()
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building

@router.put("/{building_id}", response_model=schemas.Building)
def update_building(building_id: int, building: schemas.BuildingCreate, db: Session = Depends(get_db)):
    db_building = db.query(models.Building).filter(models.Building.building_id == building_id).first()
    if db_building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    
    for key, value in building.dict().items():
        setattr(db_building, key, value)
    
    db.commit()
    db.refresh(db_building)
    return db_building

@router.delete("/{building_id}", response_model=schemas.Building)
def delete_building(building_id: int, db: Session = Depends(get_db)):
    db_building = db.query(models.Building).filter(models.Building.building_id == building_id).first()
    if db_building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    
    db.delete(db_building)
    db.commit()
    return db_building
