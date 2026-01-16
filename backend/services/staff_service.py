from sqlalchemy.orm import Session
from models.staff_model import Staff

# -------------------------------
# CRUD logic for Staff
# -------------------------------

def create_staff(db: Session, name: str, age: int, position: str):
    new_staff = Staff(name=name, age=age, position=position)
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    return new_staff

def list_staff(db: Session):
    return db.query(Staff).all()

def get_staff(db: Session, staff_id: int):
    return db.query(Staff).filter(Staff.id == staff_id).first()

def delete_staff(db: Session, staff_id: int):
    staff = get_staff(db, staff_id)
    if staff:
        db.delete(staff)
        db.commit()
        return True
    return False

def update_staff(db: Session, staff_id: int, name: str, age: int, position: str):
    staff = get_staff(db, staff_id)
    if staff:
        staff.name = name
        staff.age = age
        staff.position = position
        db.commit()
        db.refresh(staff)
        return staff
    return None

# Optional: filter by position
def filter_staff_by_position(db: Session, position: str):
    return db.query(Staff).filter(Staff.position == position).all()
