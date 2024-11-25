from fastapi import APIRouter, Depends, HTTPException, Request, Form, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, timedelta
from .. import models, schemas
from ..database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/filter")  # Move this before the /{schedule_id} route
async def filter_schedules(
    request: Request,
    status: str = Query(default="pending"),  # Add default value
    db: Session = Depends(get_db)
):
    query = db.query(models.MedicationSchedule)\
        .join(models.Patient)\
        .join(models.Medication)\
        .options(
            joinedload(models.MedicationSchedule.patient).joinedload(models.Patient.bed)
            .joinedload(models.Bed.room)
            .joinedload(models.Room.ward),
            joinedload(models.MedicationSchedule.medication)
        )
    
    if status != "all":
        query = query.filter(models.MedicationSchedule.is_completed == (status == "completed"))
    
    schedules = query.order_by(models.MedicationSchedule.schedule_time).all()
    return templates.TemplateResponse(
        "schedules/_list.html",
        {"request": request, "schedules": schedules}
    )

@router.get("/list", response_class=HTMLResponse)
def get_schedules_list(request: Request, db: Session = Depends(get_db)):
    schedules = db.query(models.MedicationSchedule)\
        .join(models.Patient)\
        .join(models.Medication)\
        .filter(models.MedicationSchedule.is_completed == False)\
        .options(
            joinedload(models.MedicationSchedule.patient).joinedload(models.Patient.bed)
            .joinedload(models.Bed.room)
            .joinedload(models.Room.ward),
            joinedload(models.MedicationSchedule.medication)
        )\
        .order_by(models.MedicationSchedule.schedule_time)\
        .all()
    return templates.TemplateResponse(
        "schedules/_list.html",
        {"request": request, "schedules": schedules}
    )

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
    take_time_number: int = Form(...),  # Add this
    duration_hours: int = Form(...),    # Add this
    note: str = Form(None),
    db: Session = Depends(get_db)
):
    base_time = datetime.fromisoformat(schedule_time)
    schedules_to_create = []
    
    # Calculate schedule times based on take_time_number and duration
    for i in range(take_time_number):
        schedule_time = base_time + timedelta(hours=(duration_hours * i))
        schedule_data = {
            "patient_id": patient_id,
            "med_id": med_id,
            "schedule_time": schedule_time,
            "note": note,
            "status": "pending",
            "is_completed": False,
            "take_time_number": i + 1
        }
        schedules_to_create.append(models.MedicationSchedule(**schedule_data))
    
    # Bulk create all schedules
    db.add_all(schedules_to_create)
    db.commit()
    for schedule in schedules_to_create:
        db.refresh(schedule)
    
    # Get updated schedules list
    schedules = db.query(models.MedicationSchedule)\
        .join(models.Patient)\
        .join(models.Medication)\
        .filter(models.MedicationSchedule.is_completed == False)\
        .options(
            joinedload(models.MedicationSchedule.patient).joinedload(models.Patient.bed)
            .joinedload(models.Bed.room)
            .joinedload(models.Room.ward),
            joinedload(models.MedicationSchedule.medication)
        )\
        .order_by(models.MedicationSchedule.schedule_time)\
        .all()
    
    return templates.TemplateResponse(
        "schedules/_list.html",
        {"request": request, "schedules": schedules}
    )

@router.get("/upcoming", response_class=HTMLResponse)
async def get_upcoming_schedules(
    request: Request,
    duration_hours: int = Query(1, alias="duration"),
    db: Session = Depends(get_db)
):
    current_time = datetime.now()
    end_time = current_time + timedelta(hours=duration_hours)
    
    # Only include upcoming schedules within the time window
    schedules = db.query(models.MedicationSchedule)\
        .join(models.Patient)\
        .join(models.Medication)\
        .filter(
            models.MedicationSchedule.schedule_time >= current_time,
            models.MedicationSchedule.schedule_time <= end_time,
            models.MedicationSchedule.is_completed == False
        )\
        .options(
            joinedload(models.MedicationSchedule.patient)
            .joinedload(models.Patient.bed)
            .joinedload(models.Bed.room)
            .joinedload(models.Room.ward),
            joinedload(models.MedicationSchedule.medication)
        )\
        .order_by(models.MedicationSchedule.schedule_time)\
        .all()
        
    return templates.TemplateResponse(
        "components/upcoming_schedules.html",
        {
            "request": request,
            "schedules": schedules,
            "current_time": current_time
        }
    )

@router.get("/overdue", response_class=HTMLResponse)
async def get_overdue_schedules(
    request: Request,
    db: Session = Depends(get_db)
):
    current_time = datetime.now()
    
    schedules = db.query(models.MedicationSchedule)\
        .join(models.Patient)\
        .join(models.Medication)\
        .filter(
            models.MedicationSchedule.schedule_time < current_time,
            models.MedicationSchedule.is_completed == False
        )\
        .options(
            joinedload(models.MedicationSchedule.patient)
            .joinedload(models.Patient.bed),
            joinedload(models.MedicationSchedule.medication)
        )\
        .order_by(models.MedicationSchedule.schedule_time)\
        .all()
        
    return templates.TemplateResponse(
        "components/overdue_schedules.html",
        {
            "request": request,
            "schedules": schedules,
            "current_time": current_time
        }
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

@router.post("/{schedule_id}/complete")
def complete_schedule(
    request: Request,
    schedule_id: int, 
    db: Session = Depends(get_db)
):
    # Get schedule with relationships
    schedule = db.query(models.MedicationSchedule)\
        .filter(models.MedicationSchedule.schedule_id == schedule_id)\
        .first()
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    # Update schedule
    schedule.is_completed = True
    schedule.status = "completed"
    schedule.updated_at = datetime.now()
    db.commit()
    
    # Create history entry with nurse ID (you might want to get this from auth)
    history = models.MedicationHistory(
        schedule_id=schedule_id,
        given_time=datetime.now(),
        status="completed",
        given_by=1,  # TODO: Replace with actual nurse ID from authentication
        note="Medication administered"
    )
    db.add(history)
    db.commit()
    
    # Get updated schedules list with relationships
    schedules = db.query(models.MedicationSchedule)\
        .join(models.Patient)\
        .join(models.Medication)\
        .options(
            joinedload(models.MedicationSchedule.patient).joinedload(models.Patient.bed)
            .joinedload(models.Bed.room)
            .joinedload(models.Room.ward),
            joinedload(models.MedicationSchedule.medication)
        )\
        .all()
    
    return templates.TemplateResponse(
        "schedules/_list.html",
        {"request": request, "schedules": schedules}
    )