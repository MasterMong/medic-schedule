-- สร้างตารางอาคาร
CREATE TABLE buildings (
    building_id INT PRIMARY KEY AUTO_INCREMENT,
    building_name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- สร้างตารางชั้น
CREATE TABLE floors (
    floor_id INT PRIMARY KEY AUTO_INCREMENT,
    building_id INT,
    floor_number VARCHAR(20) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (building_id) REFERENCES buildings(building_id)
);

-- สร้างตารางวอร์ด
CREATE TABLE wards (
    ward_id INT PRIMARY KEY AUTO_INCREMENT,
    ward_name VARCHAR(100) NOT NULL,
    ward_type VARCHAR(50),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- สร้างตารางห้อง
CREATE TABLE rooms (
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    floor_id INT,
    ward_id INT,
    room_number VARCHAR(20) NOT NULL,
    room_type VARCHAR(50),
    capacity INT,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (floor_id) REFERENCES floors(floor_id),
    FOREIGN KEY (ward_id) REFERENCES wards(ward_id)
);

-- สร้างตารางเตียง
CREATE TABLE beds (
    bed_id INT PRIMARY KEY AUTO_INCREMENT,
    room_id INT,
    bed_number VARCHAR(20) NOT NULL,
    bed_type VARCHAR(50),
    is_occupied BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (room_id) REFERENCES rooms(room_id)
);

-- สร้างตารางพยาบาล
CREATE TABLE nurses (
    nurse_id INT PRIMARY KEY AUTO_INCREMENT,
    ward_id INT,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(50),
    shift VARCHAR(20),
    contact VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (ward_id) REFERENCES wards(ward_id)
);

-- สร้างตารางผู้ป่วย
CREATE TABLE patients (
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    bed_id INT,
    hn VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    dob DATE,
    admission_date DATE,
    diagnosis TEXT,
    allergies TEXT,
    status VARCHAR(50),
    FOREIGN KEY (bed_id) REFERENCES beds(bed_id)
);

-- สร้างตารางยา
CREATE TABLE medications (
    med_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50),
    route VARCHAR(50),
    unit VARCHAR(20),
    instruction TEXT,
    frequency VARCHAR(50),
    special_instruction TEXT
);

-- สร้างตาราง Preset การให้ยา
CREATE TABLE medication_presets (
    preset_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    condition_text TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- สร้างตารางตารางการให้ยา
CREATE TABLE medication_schedules (
    schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT,
    nurse_id INT,
    med_id INT,
    schedule_time DATETIME,
    status VARCHAR(50),
    note TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (nurse_id) REFERENCES nurses(nurse_id),
    FOREIGN KEY (med_id) REFERENCES medications(med_id)
);

-- สร้างตารางประวัติการให้ยา
CREATE TABLE medication_history (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    schedule_id INT,
    given_time DATETIME,
    status VARCHAR(50),
    note TEXT,
    given_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (schedule_id) REFERENCES medication_schedules(schedule_id),
    FOREIGN KEY (given_by) REFERENCES nurses(nurse_id)
);

-- สร้าง Index เพื่อเพิ่มประสิทธิภาพการค้นหา
CREATE INDEX idx_patient_hn ON patients(hn);
CREATE INDEX idx_schedule_time ON medication_schedules(schedule_time);
CREATE INDEX idx_med_status ON medication_schedules(status);
CREATE INDEX idx_nurse_shift ON nurses(shift);