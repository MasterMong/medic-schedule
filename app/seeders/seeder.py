from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from .. import models

def seed_data(db: Session):
    # Clear existing data (optional)
    clear_tables(db)
    
    # Seed buildings
    building = models.Building(
        building_name="Main Hospital Building",
        description="Main hospital facility with 5 floors"
    )
    db.add(building)
    db.commit()
    
    # Seed floors
    floors = []
    for i in range(1, 6):
        floor = models.Floor(
            building_id=building.building_id,
            floor_number=str(i),
            description=f"Floor {i}"
        )
        db.add(floor)
        floors.append(floor)
    db.commit()
    
    # Seed wards
    wards = [
        models.Ward(ward_name="Medical Ward", ward_type="Medical"),
        models.Ward(ward_name="Surgical Ward", ward_type="Surgical"),
        models.Ward(ward_name="Pediatric Ward", ward_type="Pediatric")
    ]
    db.add_all(wards)
    db.commit()
    
    # Seed rooms
    rooms = []
    for floor in floors:
        for i in range(1, 5):
            room = models.Room(
                floor_id=floor.floor_id,
                ward_id=wards[i % len(wards)].ward_id,
                room_number=f"{floor.floor_number}{str(i).zfill(2)}",
                room_type="Standard",
                capacity=4
            )
            db.add(room)
            rooms.append(room)
    db.commit()
    
    # Seed beds
    for room in rooms:
        for i in range(1, room.capacity + 1):
            bed = models.Bed(
                room_id=room.room_id,
                bed_number=f"{room.room_number}-{i}",
                bed_type="Standard"
            )
            db.add(bed)
    db.commit()
    
    # Seed nurses
    shifts = ["Morning", "Afternoon", "Night"]
    for ward in wards:
        for i in range(1, 4):
            nurse = models.Nurse(
                ward_id=ward.ward_id,
                name=f"Nurse {ward.ward_name} {i}",
                position="Registered Nurse",
                shift=shifts[i % len(shifts)],
                contact=f"ext-{1000 + i}"
            )
            db.add(nurse)
    db.commit()
    
    # Seed medications
    medications = [
        models.Medication(
            name="Paracetamol",
            type="Analgesic",
            route="Oral",
            unit="500mg",
            instruction="Take with water",
            frequency="Every 6 hours"
        ),
        models.Medication(
            name="Amoxicillin",
            type="Antibiotic",
            route="Oral",
            unit="250mg",
            instruction="Take after meal",
            frequency="Every 8 hours"
        ),
        models.Medication(
            name="Ibuprofen",
            type="NSAID",
            route="Oral",
            unit="400mg",
            instruction="Take with food",
            frequency="Every 8 hours"
        )
    ]
    db.add_all(medications)
    db.commit()

    # Seed medication presets
    presets = [
        models.MedicationPreset(
            name="Post-Surgery Pain Management",
            description="Standard pain management protocol after surgery",
            condition_text="Post-operative pain",
            common_instruction="Adjust dosage based on pain level"
        ),
        models.MedicationPreset(
            name="Basic Fever Treatment",
            description="Standard protocol for fever management",
            condition_text="Fever above 38°C",
            common_instruction="Monitor temperature every 4 hours"
        )
    ]
    db.add_all(presets)
    db.commit()

    # Seed preset medications
    preset_meds = [
        models.PresetMedication(
            preset_id=presets[0].preset_id,
            med_id=medications[0].med_id,  # Paracetamol
            dosage="1000mg",
            frequency="Every 6 hours",
            duration="3 days",
            special_instruction="Take with food"
        ),
        models.PresetMedication(
            preset_id=presets[0].preset_id,
            med_id=medications[2].med_id,  # Ibuprofen
            dosage="400mg",
            frequency="Every 8 hours",
            duration="3 days",
            special_instruction="Take after meals"
        )
    ]
    db.add_all(preset_meds)
    db.commit()

    # Seed some test patients
    patients = [
        models.Patient(
            bed_id=1,  # Assuming bed with ID 1 exists
            hn="HN001",
            name="John Doe",
            dob=date(1990, 1, 1),
            admission_date=date.today(),
            diagnosis="Fever",
            status="Admitted"
        ),
        models.Patient(
            bed_id=2,  # Assuming bed with ID 2 exists
            hn="HN002",
            name="Jane Smith",
            dob=date(1985, 5, 15),
            admission_date=date.today(),
            diagnosis="Post-surgery recovery",
            status="Admitted"
        )
    ]
    db.add_all(patients)
    db.commit()

    # Seed medication schedules
    current_time = datetime.now()
    schedules = [
        models.MedicationSchedule(
            patient_id=patients[0].patient_id,
            nurse_id=1,  # Assuming nurse with ID 1 exists
            med_id=medications[0].med_id,
            take_time_number=1,
            schedule_time=current_time + timedelta(hours=6),
            status="Scheduled"
        ),
        models.MedicationSchedule(
            patient_id=patients[0].patient_id,
            nurse_id=1,
            med_id=medications[0].med_id,
            take_time_number=2,
            schedule_time=current_time + timedelta(hours=12),
            status="Scheduled"
        )
    ]
    db.add_all(schedules)
    db.commit()

def clear_tables(db: Session):
    # Delete in reverse order of dependencies
    db.query(models.MedicationHistory).delete()
    db.query(models.MedicationSchedule).delete()
    db.query(models.MedicationPreset).delete()
    db.query(models.Patient).delete()
    db.query(models.Medication).delete()
    db.query(models.Nurse).delete()
    db.query(models.Bed).delete()
    db.query(models.Room).delete()
    db.query(models.Ward).delete()
    db.query(models.Floor).delete()
    db.query(models.Building).delete()
    db.query(models.PresetMedication).delete()
    db.query(models.MedicationPreset).delete()
    db.commit()