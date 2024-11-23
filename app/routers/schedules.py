from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.MedicationSchedule])
def get_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    schedules = db.query(models.MedicationSchedule).offset(skip).limit(limit).all()
    return schedules

@router.post("/", response_model=schemas.MedicationSchedule)
def create_schedule(schedule: schemas.MedicationScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = models.MedicationSchedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.put("/{schedule_id}/complete", response_model=schemas.MedicationSchedule)
def complete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.MedicationSchedule).filter(models.MedicationSchedule.schedule_id == schedule_id).first()
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    schedule.is_completed = True
    db.commit()
    db.refresh(schedule)
    return schedule

@router.get("/{schedule_id}", response_model=schemas.MedicationSchedule)
def get_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.MedicationSchedule).filter(models.MedicationSchedule.schedule_id == schedule_id).first()
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@router.put("/{schedule_id}", response_model=schemas.MedicationSchedule)
def update_schedule(schedule_id: int, schedule: schemas.MedicationScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = db.query(models.MedicationSchedule).filter(models.MedicationSchedule.schedule_id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    for key, value in schedule.dict().items():
        setattr(db_schedule, key, value)
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.delete("/{schedule_id}")
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.MedicationSchedule).filter(models.MedicationSchedule.schedule_id == schedule_id).first()
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    db.delete(schedule)
    db.commit()
    return {"message": "Schedule deleted successfully"}