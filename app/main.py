from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import (
    buildings, floors, wards, rooms, beds,
    nurses, patients, medications,
    medication_presets, medication_schedules, medication_history, 
    preset_medications, admin  # Add preset_medications here
)
from .database import engine, SessionLocal
from . import models
from .seeders.seeder import seed_data

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Medication Tracking System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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