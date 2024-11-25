from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from .. import models

def seed_data(db: Session):
    # Clear existing data (optional)
    clear_tables(db)
    
    # Seed buildings
    building = models.Building(
        building_name="ตึก 20",
        description="ตึก 20 มีทั้งหมด 5 ชั้น"
    )
    db.add(building)
    db.commit()
    
    # Seed floors
    floors = []
    for i in range(1, 6):
        floor = models.Floor(
            building_id=building.building_id,
            floor_number=str(i),
            description=f"ชั้น {i}"
        )
        db.add(floor)
        floors.append(floor)
    db.commit()

    # Seed wards
    wards = [
        models.Ward(
            ward_name="กุมารเวชกรรม",
            ward_type="กุมารเวชกรรม"
        ),
        models.Ward(
            ward_name="จิตเวช",
            ward_type="จิตเวช"
        ),
        models.Ward(
            ward_name="จักษุ",
            ward_type="จักษุ"
        ),
        models.Ward(
            ward_name="ทารกแรกเกิด (NICU)",
            ward_type="ทารกแรกเกิด"
        ),
        models.Ward(
            ward_name="ไตเทียม",
            ward_type="ไตเทียม"
        ),
        models.Ward(
            ward_name="ประสาทวิทยา",
            ward_type="ประสาทวิทยา"
        ),
        models.Ward(
            ward_name="มะเร็ง",
            ward_type="มะเร็งวิทยา"
        ),
        models.Ward(
            ward_name="เวชศาสตร์ฟื้นฟู",
            ward_type="เวชศาสตร์ฟื้นฟู"
        ),
        models.Ward(
            ward_name="แยกโรคติดเชื้อ",
            ward_type="โรคติดเชื้อ"
        ),
        models.Ward(
            ward_name="โสต ศอ นาสิก",
            ward_type="โสต ศอ นาสิก"
        ),
        models.Ward(
            ward_name="ศัลยกรรม",
            ward_type="ศัลยกรรม"
        ),
        models.Ward(
            ward_name="ศัลยกรรมทรวงอก",
            ward_type="ศัลยกรรมทรวงอก"
        ),
        models.Ward(
            ward_name="ศัลยกรรมระบบประสาท",
            ward_type="ศัลยกรรมประสาท"
        ),
        models.Ward(
            ward_name="สูติ-นรีเวชกรรม",
            ward_type="สูติ-นรีเวชกรรม"
        ),
        models.Ward(
            ward_name="หนัก (ICU)",
            ward_type="วิกฤต"
        ),
        models.Ward(
            ward_name="หนักโรคหัวใจ (CCU)",
            ward_type="วิกฤต"
        ),
        models.Ward(
            ward_name="ออร์โธปิดิกส์",
            ward_type="ออร์โธปิดิกส์"
        ),
        models.Ward(
            ward_name="อายุรกรรม",
            ward_type="อายุรกรรม"
        ),
        models.Ward(
            ward_name="อายุรกรรมระบบประสาท",
            ward_type="ประสาทวิทยา"
        ),
        models.Ward(
            ward_name="อายุรกรรมโรคปอด",
            ward_type="อายุรกรรมปอด"
        ),
        models.Ward(
            ward_name="อุบัติเหตุฉุกเฉิน",
            ward_type="อุบัติเหตุฉุกเฉิน"
        )
    ]

    db.add_all(wards)
    db.commit()
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
                room_type="ปกติ",
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
                bed_type="ปกติ"
            )
            db.add(bed)
    db.commit()
    
    # Seed nurses
    shifts = ["เช้า", "บ่าย", "ดึก"]
    for ward in wards:
        for i in range(1, 4):
            nurse = models.Nurse(
                ward_id=ward.ward_id,
                name=f"พยาบาล {ward.ward_name} {i}",
                position="พยาบาล",
                shift=shifts[i % len(shifts)],
                contact=f"ext-{1000 + i}"
            )
            db.add(nurse)
    db.commit()
    
    # Seed medications
    medications = [
        models.Medication(
            name="พาราเซตามอล",
            type="ยาแก้ปวดลดไข้",
            route="รับประทาน",
            unit="500มก.",
            instruction="รับประทานพร้อมน้ำ",
            frequency="ทุก 6 ชั่วโมง"
        ),
        models.Medication(
            name="อะม็อกซิซิลลิน",
            type="ยาปฏิชีวนะ",
            route="รับประทาน",
            unit="250มก.",
            instruction="รับประทานหลังอาหาร",
            frequency="ทุก 8 ชั่วโมง"
        ),
        models.Medication(
            name="ไอบูโพรเฟน",
            type="ยาต้านการอักเสบที่ไม่ใช่สเตียรอยด์",
            route="รับประทาน",
            unit="400มก.",
            instruction="รับประทานพร้อมอาหาร",
            frequency="ทุก 8 ชั่วโมง"
        ),
        models.Medication(
            name="โอเมพราโซล",
            type="ยาลดกรดในกระเพาะอาหาร",
            route="รับประทาน",
            unit="20มก.",
            instruction="รับประทานก่อนอาหาร",
            frequency="วันละ 1 ครั้ง"
        ),
        models.Medication(
            name="ซิทิริซิน",
            type="ยาแก้แพ้",
            route="รับประทาน",
            unit="10มก.",
            instruction="รับประทานก่อนนอน",
            frequency="วันละ 1 ครั้ง"
        ),
        models.Medication(
            name="เมทฟอร์มิน",
            type="ยาเบาหวาน",
            route="รับประทาน",
            unit="500มก.",
            instruction="รับประทานพร้อมอาหาร",
            frequency="วันละ 2 ครั้ง"
        ),
        models.Medication(
            name="อะทอร์วาสแตติน",
            type="ยาลดไขมัน",
            route="รับประทาน",
            unit="20มก.",
            instruction="รับประทานก่อนนอน",
            frequency="วันละ 1 ครั้ง"
        ),
        models.Medication(
            name="โลซาร์แทน",
            type="ยาความดันโลหิตสูง",
            route="รับประทาน",
            unit="50มก.",
            instruction="รับประทานหลังอาหารเช้า",
            frequency="วันละ 1 ครั้ง"
        ),
        models.Medication(
            name="เซอร์ทราลีน",
            type="ยารักษาโรคซึมเศร้า",
            route="รับประทาน",
            unit="50มก.",
            instruction="รับประทานหลังอาหารเช้า",
            frequency="วันละ 1 ครั้ง"
        ),
        models.Medication(
            name="มอนเทลูคาสท์",
            type="ยาแก้แพ้",
            route="รับประทาน",
            unit="10มก.",
            instruction="รับประทานก่อนนอน",
            frequency="วันละ 1 ครั้ง"
        ),
        models.Medication(
            name="เลโวไทร็อกซิน",
            type="ยาไทรอยด์",
            route="รับประทาน",
            unit="100มคก.",
            instruction="รับประทานก่อนอาหารเช้า",
            frequency="วันละ 1 ครั้ง"
        ),
        models.Medication(
            name="ไดคลอฟีแนค",
            type="ยาแก้ปวดลดการอักเสบ",
            route="รับประทาน",
            unit="25มก.",
            instruction="รับประทานหลังอาหาร",
            frequency="ทุก 8 ชั่วโมง"
        ),
        models.Medication(
            name="คลอเฟนิรามีน",
            type="ยาแก้แพ้",
            route="รับประทาน",
            unit="4มก.",
            instruction="รับประทานก่อนนอน",
            frequency="วันละ 1 ครั้ง"
        ),
        models.Medication(
            name="แอมบรอกซอล",
            type="ยาละลายเสมหะ",
            route="รับประทาน",
            unit="30มก.",
            instruction="รับประทานหลังอาหาร",
            frequency="วันละ 3 ครั้ง"
        ),
        models.Medication(
            name="ดอมเพอริโดน",
            type="ยาแก้คลื่นไส้",
            route="รับประทาน",
            unit="10มก.",
            instruction="รับประทานก่อนอาหาร",
            frequency="วันละ 3 ครั้ง"
        ),
        models.Medication(
            name="ไฮโดรคลอโรไทอาไซด์",
            type="ยาขับปัสสาวะ",
            route="รับประทาน",
            unit="25มก.",
            instruction="รับประทานหลังอาหารเช้า",
            frequency="วันละ 1 ครั้ง"
        ),
        models.Medication(
            name="กาบาเพนติน",
            type="ยารักษาโรคลมชัก",
            route="รับประทาน",
            unit="300มก.",
            instruction="รับประทานก่อนนอน",
            frequency="วันละ 1 ครั้ง"
        ),
        models.Medication(
            name="ไซโลเฟน",
            type="ยาคลายกล้ามเนื้อ",
            route="รับประทาน",
            unit="500มก.",
            instruction="รับประทานหลังอาหาร",
            frequency="วันละ 3 ครั้ง"
        ),
        models.Medication(
            name="เฟกโซเฟนาดีน",
            type="ยาแก้แพ้",
            route="รับประทาน",
            unit="60มก.",
            instruction="รับประทานก่อนอาหาร",
            frequency="วันละ 2 ครั้ง"
        ),
        models.Medication(
            name="คาร์บามาเซพีน",
            type="ยากันชัก",
            route="รับประทาน",
            unit="200มก.",
            instruction="รับประทานพร้อมอาหาร",
            frequency="วันละ 2 ครั้ง"
        ),
        models.Medication(
            name="ไรสเพอริโดน",
            type="ยารักษาโรคจิต",
            route="รับประทาน",
            unit="2มก.",
            instruction="รับประทานหลังอาหารเย็น",
            frequency="วันละ 1 ครั้ง"
        ),
        models.Medication(
            name="คอลชิซิน",
            type="ยารักษาโรคเกาต์",
            route="รับประทาน",
            unit="0.6มก.",
            instruction="รับประทานเมื่อมีอาการ",
            frequency="ตามแพทย์สั่ง"
        ),
        models.Medication(
            name="อัลลอพูรินอล",
            type="ยารักษาโรคเกาต์",
            route="รับประทาน",
            unit="100มก.",
            instruction="รับประทานหลังอาหาร",
            frequency="วันละ 1 ครั้ง"
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