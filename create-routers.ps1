$models = @(
    "Building",
    "Floor",
    "Ward",
    "Room",
    "Bed",
    "Nurse",
    "Patient",
    "Medication",
    "MedicationPreset",
    "MedicationSchedule",
    "MedicationHistory"
)

$routersPath = "./app/routers"

# Ensure routers directory exists
New-Item -ItemType Directory -Force -Path $routersPath

foreach ($model in $models) {
    $modelLower = $model.ToLower()
    $pluralName = if ($model -match ".*y$") {
        $modelLower -replace "y$", "ies"
    } elseif ($model -in @("MedicationPreset", "MedicationSchedule", "MedicationHistory")) {
        # Special case for medication-related routes to match main.py
        $modelLower.ToLower() -replace "medication", "medication-"
    } else {
        "${modelLower}s"
    }
    $idName = "${modelLower}_id"
    $routerPath = "$routersPath/$($pluralName -replace "-", "_").py"
    
    $content = @"
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.$model])
def get_$pluralName(skip`: int = 0, limit`: int = 100, db`: Session = Depends(get_db)):
    $pluralName = db.query(models.$model).offset(skip).limit(limit).all()
    return $pluralName

@router.post("/", response_model=schemas.$model)
def create_$modelLower($modelLower`: schemas.${model}Create, db`: Session = Depends(get_db)):
    db_$modelLower = models.$model(**$modelLower.dict())
    db.add(db_$modelLower)
    db.commit()
    db.refresh(db_$modelLower)
    return db_$modelLower

@router.get("/{$idName}", response_model=schemas.$model)
def get_$modelLower($idName`: int, db`: Session = Depends(get_db)):
    $modelLower = db.query(models.$model).filter(models.$model.$idName == $idName).first()
    if $modelLower is None:
        raise HTTPException(status_code=404, detail="$model not found")
    return $modelLower
"@

    Set-Content -Path $routerPath -Value $content
    Write-Host "Created router file: $routerPath"
}
