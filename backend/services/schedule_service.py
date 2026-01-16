from sqlalchemy.orm import Session
from datetime import date, timedelta
import csv
from sqlalchemy.orm import Session, joinedload
from models.staff_model import Staff
from models.schedule_model import Schedule
from fastapi import HTTPException

# -------------------------------
# Manual CRUD
# -------------------------------

# def create_schedule(db: Session, staff_id: int, duty_date: date):
#     new_schedule = Schedule(staff_id=staff_id, duty_date=duty_date)
#     db.add(new_schedule)
#     db.commit()

#     return (
#         db.query(Schedule)
#         .options(joinedload(Schedule.staff))
#         .filter(Schedule.id == new_schedule.id)
#         .first()
#     )

def create_schedule(db: Session, staff_id: int, duty_date: date):
    # 1. Check if an assignment already exists for this staff on this date
    existing_schedule = db.query(Schedule).filter(
        Schedule.staff_id == staff_id,
        Schedule.duty_date == duty_date
    ).first()

    # 2. If it exists, stop and raise an error
    if existing_schedule:
        # We use 400 (Bad Request) so the frontend knows it's a validation error
        raise HTTPException(
            status_code=400, 
            detail="This staff member is already assigned to a duty on this date."
        )

    # 3. If no duplicate, proceed with creation
    new_schedule = Schedule(staff_id=staff_id, duty_date=duty_date)
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule) # Refresh to get the auto-generated ID

    # 4. Return with joined staff data for the frontend
    return (
        db.query(Schedule)
        .options(joinedload(Schedule.staff))
        .filter(Schedule.id == new_schedule.id)
        .first()
    )
    
def list_schedules(db: Session):
    return (
        db.query(Schedule)
        .options(joinedload(Schedule.staff))
        .all()
    )

def delete_schedule(db: Session, schedule_id: int):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if schedule:
        db.delete(schedule)
        db.commit()
        return True
    return False

def update_schedule(db: Session, schedule_id: int, staff_id: int, duty_date: date):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        return None

    schedule.staff_id = staff_id
    schedule.duty_date = duty_date
    db.commit()

    return (
        db.query(Schedule)
        .options(joinedload(Schedule.staff))
        .filter(Schedule.id == schedule_id)
        .first()
    )

# -------------------------------
# Auto-scheduling
# -------------------------------

def auto_schedule(db: Session, start_date: date, end_date: date):
    ## to be implemented 
    return {"message": f"Schedules created for {start_date} to {end_date}"}

# -------------------------------
# Export schedules
# -------------------------------

def export_schedule(db: Session, filename="schedules.csv"):
    schedules = (
        db.query(Schedule)
        .options(joinedload(Schedule.staff))
        .all()
    )

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Schedule ID", "Staff ID", "Staff Name", "Duty Date"])

        for s in schedules:
            writer.writerow([
                s.id,
                s.staff_id,
                s.staff.name if s.staff else "",
                s.duty_date
            ])

    return filename

