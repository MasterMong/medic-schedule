from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from .. import models, schemas
from ..database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=List[schemas.MedicationSchedule])
def get_medication_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    schedules = db.query(models.MedicationSchedule).offset(skip).limit(limit).all()
    return schedules

@router.post("/")
async def create_medication_schedule(
    request: Request,
    patient_id: int = Form(...),
    med_id: int = Form(...),
    schedule_time: str = Form(...),
    note: str = Form(None),
    db: Session = Depends(get_db)
):
    schedule_data = {
        "patient_id": patient_id,
        "med_id": med_id,
        "schedule_time": datetime.fromisoformat(schedule_time),
        "note": note,
        "status": "pending",
        "is_completed": False
    }
    
    db_schedule = models.MedicationSchedule(**schedule_data)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    
    schedules = db.query(models.MedicationSchedule).all()
    return templates.TemplateResponse(
        "schedules/_list.html",
        {"request": request, "schedules": schedules}
    )

@router.get("/{schedule_id}", response_model=schemas.MedicationSchedule)
def get_medication_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.MedicationSchedule).filter(models.MedicationSchedule.schedule_id == schedule_id).first()
    if schedule is None:
        raise HTTPException(status_code=404, detail="Medication schedule not found")
    return schedule

@router.put("/{schedule_id}", response_model=schemas.MedicationSchedule)
def update_medication_schedule(schedule_id: int, schedule: schemas.MedicationScheduleCreate, db: Session = Depends(get_db)):
    db_schedule = db.query(models.MedicationSchedule).filter(models.MedicationSchedule.schedule_id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Medication schedule not found")
    
    for key, value in schedule.dict().items():
        setattr(db_schedule, key, value)
    
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

@router.delete("/{schedule_id}", response_model=schemas.MedicationSchedule)
def delete_medication_schedule(schedule_id: int, db: Session = Depends(get_db)):
    db_schedule = db.query(models.MedicationSchedule).filter(models.MedicationSchedule.schedule_id == schedule_id).first()
    if db_schedule is None:
        raise HTTPException(status_code=404, detail="Medication schedule not found")
    
    db.delete(db_schedule)
    db.commit()
    return db_schedule

@router.post("/complete/{schedule_id}")
def complete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = db.query(models.MedicationSchedule).filter(models.MedicationSchedule.schedule_id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    schedule.is_completed = True
    db.commit()
    
    # Create history entry
    history = models.MedicationHistory(
        schedule_id=schedule_id,
        given_time=datetime.now(),
        status="completed"
    )
    db.add(history)
    db.commit()
    
    return {"message": "Schedule completed"}

@router.get("/filter")
def filter_schedules(request: Request, status: str, db: Session = Depends(get_db)):
    query = db.query(models.MedicationSchedule)
    
    if status == "pending":
        query = query.filter(models.MedicationSchedule.is_completed == False)
    elif status == "completed":
        query = query.filter(models.MedicationSchedule.is_completed == True)
    
    schedules = query.all()
    return templates.TemplateResponse(
        "schedules/_list.html",
        {"request": request, "schedules": schedules}
    )

@router.get("/list", response_class=HTMLResponse)
def get_schedules_list(request: Request, db: Session = Depends(get_db)):
    schedules = db.query(models.MedicationSchedule).all()
    return templates.TemplateResponse(
        "schedules/_list.html",
        {"request": request, "schedules": schedules}
    )