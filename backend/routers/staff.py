from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db        
from services.staff_service import (
    create_staff,
    list_staff,
    get_staff,
    delete_staff,
    update_staff,
    filter_staff_by_position
)
from schemas.staff_schema import StaffCreate, StaffResponse

router = APIRouter(prefix="/staff", tags=["staff"])

# -------------------------------
# Endpoints
# -------------------------------

# List all staff
@router.get("/", response_model=list[StaffResponse])
def get_all_staff(db: Session = Depends(get_db)):
    return list_staff(db)

# Create new staff
@router.post("/", response_model=StaffResponse)
def create_staff_endpoint(staff: StaffCreate, db: Session = Depends(get_db)):
    return create_staff(db, staff.name, staff.age, staff.position)

# Get a single staff member
@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff_endpoint(staff_id: int, db: Session = Depends(get_db)):
    staff = get_staff(db, staff_id)
    if staff:
        return staff
    raise HTTPException(status_code=404, detail="Staff not found")

# Delete staff
@router.delete("/{staff_id}")
def delete_staff_endpoint(staff_id: int, db: Session = Depends(get_db)):
    success = delete_staff(db, staff_id)
    if success:
        return {"message": "Staff deleted successfully"}
    raise HTTPException(status_code=404, detail="Staff not found")

# Update staff
@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff_endpoint(staff_id: int, staff: StaffCreate, db: Session = Depends(get_db)):
    updated = update_staff(db, staff_id, staff.name, staff.age, staff.position)
    if updated:
        return updated
    raise HTTPException(status_code=404, detail="Staff not found")

# Filter staff by position (optional)
@router.get("/position/{position}", response_model=list[StaffResponse])
def filter_staff_endpoint(position: str, db: Session = Depends(get_db)):
    return filter_staff_by_position(db, position)
