from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class BuildingBase(BaseModel):
    building_name: str
    description: Optional[str] = None
    is_active: bool = True

class BuildingCreate(BuildingBase):
    pass

class Building(BuildingBase):
    building_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class FloorBase(BaseModel):
    building_id: int
    floor_number: str
    description: Optional[str] = None
    is_active: bool = True

class FloorCreate(FloorBase):
    pass

class Floor(FloorBase):
    floor_id: int

    class Config:
        orm_mode = True

class WardBase(BaseModel):
    ward_name: str
    ward_type: Optional[str] = None
    description: Optional[str] = None
    is_active: bool = True

class WardCreate(WardBase):
    pass

class Ward(WardBase):
    ward_id: int

    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    floor_id: int
    ward_id: int
    room_number: str
    room_type: Optional[str] = None
    capacity: Optional[int] = None
    is_active: bool = True

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    room_id: int

    class Config:
        orm_mode = True

class BedBase(BaseModel):
    room_id: int
    bed_number: str
    bed_type: Optional[str] = None
    is_occupied: bool = False
    is_active: bool = True

class BedCreate(BedBase):
    pass

class Bed(BedBase):
    bed_id: int

    class Config:
        orm_mode = True

class NurseBase(BaseModel):
    ward_id: int
    name: str
    position: Optional[str] = None
    shift: Optional[str] = None
    contact: Optional[str] = None
    is_active: bool = True

class NurseCreate(NurseBase):
    pass

class Nurse(NurseBase):
    nurse_id: int

    class Config:
        orm_mode = True

class PatientBase(BaseModel):
    bed_id: int
    hn: str
    name: str
    dob: Optional[date] = None
    admission_date: Optional[date] = None
    diagnosis: Optional[str] = None
    allergies: Optional[str] = None
    status: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    patient_id: int

    class Config:
        orm_mode = True

class MedicationBase(BaseModel):
    name: str
    type: Optional[str] = None
    route: Optional[str] = None
    unit: Optional[str] = None
    instruction: Optional[str] = None
    frequency: Optional[str] = None
    special_instruction: Optional[str] = None

class MedicationCreate(MedicationBase):
    pass

class Medication(MedicationBase):
    med_id: int

    class Config:
        orm_mode = True

class PresetMedicationBase(BaseModel):
    med_id: int
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration: Optional[str] = None
    special_instruction: Optional[str] = None

class PresetMedicationCreate(PresetMedicationBase):
    pass

class PresetMedication(PresetMedicationBase):
    preset_med_id: int
    preset_id: int

    class Config:
        orm_mode = True

class MedicationPresetBase(BaseModel):
    name: str
    description: Optional[str] = None
    condition_text: Optional[str] = None
    common_instruction: Optional[str] = None
    is_active: bool = True

class MedicationPresetCreate(MedicationPresetBase):
    medications: List[PresetMedicationCreate]

class MedicationPreset(MedicationPresetBase):
    preset_id: int
    medications: List[PresetMedication]

    class Config:
        orm_mode = True

class MedicationScheduleBase(BaseModel):
    patient_id: int
    nurse_id: Optional[int] = None  # Changed to Optional
    med_id: int
    take_time_number: int = 1
    schedule_time: datetime
    status: Optional[str] = None
    note: Optional[str] = None
    is_completed: bool = False
    updated_at: Optional[datetime] = None

class MedicationScheduleCreate(MedicationScheduleBase):
    pass

class MedicationSchedule(MedicationScheduleBase):
    schedule_id: int

    class Config:
        orm_mode = True

class MedicationHistoryBase(BaseModel):
    schedule_id: int
    given_time: datetime
    status: Optional[str] = None
    note: Optional[str] = None
    given_by: int

class MedicationHistoryCreate(MedicationHistoryBase):
    pass

class MedicationHistory(MedicationHistoryBase):
    history_id: int
    created_at: datetime

    class Config:
        orm_mode = True