from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from datetime import datetime  # Add this
from sqlalchemy import func  # Add this
from .routers import (
    buildings, floors, wards, rooms, beds,
    nurses, patients, medications,
    medication_presets, medication_schedules, medication_history, 
    preset_medications, admin  # Add preset_medications here
)
from .database import engine, SessionLocal
from . import models
from .seeders.seeder import seed_data
from sqlalchemy.orm import joinedload

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Medication Tracking System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="templates")

app.include_router(buildings.router, prefix="/api/buildings", tags=["buildings"])
app.include_router(floors.router, prefix="/api/floors", tags=["floors"])
app.include_router(wards.router, prefix="/api/wards", tags=["wards"])
app.include_router(rooms.router, prefix="/api/rooms", tags=["rooms"])
app.include_router(beds.router, prefix="/api/beds", tags=["beds"])
app.include_router(nurses.router, prefix="/api/nurses", tags=["nurses"])
app.include_router(patients.router, prefix="/api/patients", tags=["patients"])
app.include_router(medications.router, prefix="/api/medications", tags=["medications"])
app.include_router(medication_presets.router, prefix="/api/medication-presets", tags=["medication-presets"])
app.include_router(medication_schedules.router, prefix="/api/schedules", tags=["schedules"])
app.include_router(medication_history.router, prefix="/api/medication-history", tags=["medication-history"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(
    preset_medications.router, 
    prefix="/api/preset-medications", 
    tags=["preset-medications"]
)

# View routes for template rendering
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/patients", response_class=HTMLResponse)
async def patients_page(request: Request):
    patients = get_patients_from_db()  # You'll need to implement this
    return templates.TemplateResponse(
        "patients/list.html", 
        {"request": request, "patients": patients}
    )

@app.get("/schedules", response_class=HTMLResponse)
async def schedules_page(request: Request):
    db = SessionLocal()
    try:
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
        patients = db.query(models.Patient).all()
        medications = db.query(models.Medication).all()
        return templates.TemplateResponse(
            "schedules/list.html", 
            {
                "request": request, 
                "schedules": schedules,
                "patients": patients,
                "medications": medications,
                "current_status": "pending",
                "now": datetime.now()  # Add this line
            }
        )
    finally:
        db.close()

@app.get("/medications/presets", response_class=HTMLResponse)
async def presets_page(request: Request):
    presets = get_medication_presets_from_db()  # You'll need to implement this
    return templates.TemplateResponse(
        "medications/presets.html", 
        {"request": request, "presets": presets}
    )

@app.get("/medications", response_class=HTMLResponse)
async def medications_page(request: Request):
    medications = get_medications_from_db()
    return templates.TemplateResponse(
        "medications/list.html", 
        {"request": request, "medications": medications}
    )

# Helper functions to get data from database
def get_patients_from_db():
    db = SessionLocal()
    try:
        return db.query(models.Patient)\
            .join(models.Bed)\
            .join(models.Room)\
            .join(models.Ward)\
            .options(
                joinedload(models.Patient.bed),
                joinedload(models.Patient.bed).joinedload(models.Bed.room),
                joinedload(models.Patient.bed).joinedload(models.Bed.room).joinedload(models.Room.ward)
            )\
            .all()
    finally:
        db.close()

def get_schedules_from_db():
    db = SessionLocal()
    try:
        return db.query(models.MedicationSchedule)\
            .join(models.Patient)\
            .join(models.Medication)\
            .options(
                joinedload(models.MedicationSchedule.patient),
                joinedload(models.MedicationSchedule.medication)
            )\
            .all()
    finally:
        db.close()

def get_medication_presets_from_db():
    db = SessionLocal()
    try:
        return db.query(models.MedicationPreset)\
            .options(
                joinedload(models.MedicationPreset.medications)
                .joinedload(models.PresetMedication.medication)
            )\
            .all()
    finally:
        db.close()

def get_medications_from_db():
    db = SessionLocal()
    try:
        return db.query(models.Medication).all()
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Hospital Medication Tracking System API"}


# Dashboard API endpoints
@app.get("/api/dashboard/pending-count")
async def get_pending_count():
    db = SessionLocal()
    try:
        count = db.query(models.MedicationSchedule).filter(
            models.MedicationSchedule.is_completed == False
        ).count()
        return str(count)
    finally:
        db.close()

@app.get("/api/dashboard/patients-count")
async def get_patients_count():
    db = SessionLocal()
    try:
        count = db.query(models.Patient).count()
        return str(count)
    finally:
        db.close()

@app.get("/api/dashboard/today-count")
async def get_today_count():
    db = SessionLocal()
    try:
        today = datetime.now().date()
        count = db.query(models.MedicationSchedule).filter(
            func.date(models.MedicationSchedule.schedule_time) == today
        ).count()
        return str(count)
    finally:
        db.close()

@app.get("/api/dashboard/recent-activity")
async def get_recent_activity(request: Request):  # Add request parameter here
    db = SessionLocal()
    try:
        activities = db.query(models.MedicationHistory)\
            .join(models.MedicationSchedule)\
            .join(models.Patient)\
            .options(
                joinedload(models.MedicationHistory.medication_schedule)
                .joinedload(models.MedicationSchedule.patient),
                joinedload(models.MedicationHistory.medication_schedule)
                .joinedload(models.MedicationSchedule.medication),
                joinedload(models.MedicationHistory.nurse)
            )\
            .order_by(models.MedicationHistory.created_at.desc())\
            .limit(5)\
            .all()
        return templates.TemplateResponse(
            "components/recent_activity.html",
            {"request": request, "activities": activities}
        )
    finally:
        db.close()

@app.get("/seed")
async def seed_route(request: Request):
    db = SessionLocal()
    try:
        seed_data(db)
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "message": "Data seeded successfully!"}
        )
    finally:
        db.close()