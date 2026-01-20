from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db               
from services.schedule_service import (
    create_schedule,
    list_schedules,
    delete_schedule,
    update_schedule,
    export_schedule
)
from services.auto_scheduler_logic import (
    auto_schedule_logic
)
from fastapi.responses import FileResponse
from datetime import date
from schemas.schedule_schema import ScheduleCreate, ScheduleResponse

router = APIRouter(prefix="/schedule", tags=["schedule"])

# -------------------------------
# Endpoints
# -------------------------------

@router.get("/", response_model=list[ScheduleResponse])
def get_all_schedules(db: Session = Depends(get_db)):
    return list_schedules(db)

@router.post("/", response_model=ScheduleResponse)
def create_schedule_endpoint(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    return create_schedule(db, schedule.staff_id, schedule.duty_date)

@router.delete("/{schedule_id}")
def delete_schedule_endpoint(schedule_id: int, db: Session = Depends(get_db)):
    success = delete_schedule(db, schedule_id)
    if success:
        return {"message": "Schedule deleted successfully"}
    raise HTTPException(status_code=404, detail="Schedule not found")

@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule_endpoint(schedule_id: int, schedule: ScheduleCreate, db: Session = Depends(get_db)):
    updated = update_schedule(db, schedule_id, schedule.staff_id, schedule.duty_date)
    if updated:
        return updated
    raise HTTPException(status_code=404, detail="Schedule not found")

@router.post("/auto")
def auto_schedule_endpoint(
    start_date: date, 
    end_date: date, 
    db: Session = Depends(get_db)
):
    # The router manages the "Inlet" and "Outlet"
    try:
        result = auto_schedule_logic(db, start_date, end_date)
        return result
    except Exception as e:
        # If something goes wrong, the session can be rolled back here or by the dependency
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export")
def export_schedule_endpoint(db: Session = Depends(get_db)):
    filename = export_schedule(db)
    return FileResponse(path=filename, filename=filename, media_type="text/csv")
