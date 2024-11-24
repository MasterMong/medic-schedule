from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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
app.include_router(medication_schedules.router, prefix="/api/medication-schedules", tags=["medication-schedules"])
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
    schedules = get_schedules_from_db()  # You'll need to implement this
    return templates.TemplateResponse(
        "schedules/list.html", 
        {"request": request, "schedules": schedules}
    )

@app.get("/medications/presets", response_class=HTMLResponse)
async def presets_page(request: Request):
    presets = get_medication_presets_from_db()  # You'll need to implement this
    return templates.TemplateResponse(
        "medications/presets.html", 
        {"request": request, "presets": presets}
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
        return db.query(models.MedicationSchedule).all()
    finally:
        db.close()

def get_medication_presets_from_db():
    db = SessionLocal()
    try:
        return db.query(models.MedicationPreset).all()
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Hospital Medication Tracking System API"}

@app.post("/seed-data")
def seed_database():
    db = SessionLocal()
    try:
        seed_data(db)
        return {"message": "Database seeded successfully"}
    finally:
        db.close()

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
async def get_recent_activity():
    db = SessionLocal()
    try:
        activities = db.query(models.MedicationHistory)\
            .order_by(models.MedicationHistory.created_at.desc())\
            .limit(5)\
            .all()
        return templates.TemplateResponse(
            "components/recent_activity.html",
            {"request": None, "activities": activities}
        )
    finally:
        db.close()