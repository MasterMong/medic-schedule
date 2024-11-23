from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Date, DateTime, TIMESTAMP, text
from sqlalchemy.orm import relationship
from .database import Base

class Building(Base):
    __tablename__ = "buildings"
    building_id = Column(Integer, primary_key=True, index=True)
    building_name = Column(String(100), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
    floors = relationship("Floor", back_populates="building")

class Floor(Base):
    __tablename__ = "floors"
    floor_id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, ForeignKey("buildings.building_id"))
    floor_number = Column(String(20), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    building = relationship("Building", back_populates="floors")
    rooms = relationship("Room", back_populates="floor")

class Ward(Base):
    __tablename__ = "wards"
    ward_id = Column(Integer, primary_key=True, index=True)
    ward_name = Column(String(100), nullable=False)
    ward_type = Column(String(50))
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    
    rooms = relationship("Room", back_populates="ward")
    nurses = relationship("Nurse", back_populates="ward")  # Add this line

class Room(Base):
    __tablename__ = "rooms"
    room_id = Column(Integer, primary_key=True, index=True)
    floor_id = Column(Integer, ForeignKey("floors.floor_id"))
    ward_id = Column(Integer, ForeignKey("wards.ward_id"))
    room_number = Column(String(20), nullable=False)
    room_type = Column(String(50))
    capacity = Column(Integer)
    is_active = Column(Boolean, default=True)
    
    floor = relationship("Floor", back_populates="rooms")
    ward = relationship("Ward", back_populates="rooms")
    beds = relationship("Bed", back_populates="room")

class Bed(Base):
    __tablename__ = "beds"
    bed_id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.room_id"))
    bed_number = Column(String(20), nullable=False)
    bed_type = Column(String(50))
    is_occupied = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    room = relationship("Room", back_populates="beds")
    patients = relationship("Patient", back_populates="bed")

class Nurse(Base):
    __tablename__ = "nurses"
    nurse_id = Column(Integer, primary_key=True, index=True)
    ward_id = Column(Integer, ForeignKey("wards.ward_id"))
    name = Column(String(100), nullable=False)
    position = Column(String(50))
    shift = Column(String(20))
    contact = Column(String(50))
    is_active = Column(Boolean, default=True)
    
    ward = relationship("Ward", back_populates="nurses")
    medication_schedules = relationship("MedicationSchedule", back_populates="nurse")

class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(Integer, primary_key=True, index=True)
    bed_id = Column(Integer, ForeignKey("beds.bed_id"))
    hn = Column(String(20), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    dob = Column(Date)
    admission_date = Column(Date)
    diagnosis = Column(Text)
    allergies = Column(Text)
    status = Column(String(50))
    
    bed = relationship("Bed", back_populates="patients")
    medication_schedules = relationship("MedicationSchedule", back_populates="patient")

class Medication(Base):
    __tablename__ = "medications"
    med_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50))
    route = Column(String(50))
    unit = Column(String(20))
    instruction = Column(Text)
    frequency = Column(String(50))
    special_instruction = Column(Text)
    
    medication_schedules = relationship("MedicationSchedule", back_populates="medication")

class MedicationPreset(Base):
    __tablename__ = "medication_presets"
    preset_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    condition_text = Column(Text)
    is_active = Column(Boolean, default=True)

class MedicationSchedule(Base):
    __tablename__ = "medication_schedules"
    schedule_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    nurse_id = Column(Integer, ForeignKey("nurses.nurse_id"))
    med_id = Column(Integer, ForeignKey("medications.med_id"))
    schedule_time = Column(DateTime)
    status = Column(String(50))
    note = Column(Text)
    is_completed = Column(Boolean, default=False)
    updated_at = Column(TIMESTAMP)
    
    patient = relationship("Patient", back_populates="medication_schedules")
    nurse = relationship("Nurse", back_populates="medication_schedules")
    medication = relationship("Medication", back_populates="medication_schedules")
    medication_history = relationship("MedicationHistory", back_populates="medication_schedule")

class MedicationHistory(Base):
    __tablename__ = "medication_history"
    history_id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("medication_schedules.schedule_id"))
    given_time = Column(DateTime)
    status = Column(String(50))
    note = Column(Text)
    given_by = Column(Integer, ForeignKey("nurses.nurse_id"))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
    medication_schedule = relationship("MedicationSchedule", back_populates="medication_history")
    nurse = relationship("Nurse")