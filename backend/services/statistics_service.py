import calendar  
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.staff_model import Staff
from models.schedule_model import Schedule

# def get_dashboard_summary(db: Session):

def get_dashboard_summary(db: Session, target_year: int = None, target_month: int = None):
    today = date.today()
    year = target_year or today.year
    month = target_month or today.month
    
    # 1. Monthly Range Calculation
    _, num_days = calendar.monthrange(year, month)
    month_start = date(year, month, 1)
    month_end = date(year, month, num_days)

    # 2. Today's assignments (keep this based on real today)
    today_shifts = db.query(Schedule).filter(Schedule.duty_date == today).count()
    
    # 3. Personnel Utilization (STRICTLY FILTERED BY SELECTED MONTH)
    ranking_data = (
        db.query(
            Staff.id,
            Staff.name,
            Staff.position,
            func.count(Schedule.id).label("shift_count")
        )
        .outerjoin(
            Schedule, 
            (Staff.id == Schedule.staff_id) & 
            (Schedule.duty_date >= month_start) & 
            (Schedule.duty_date <= month_end)
        )
        .group_by(Staff.id)
        .order_by(func.count(Schedule.id).desc(), Staff.name.asc())
        .all()
    )
    
    ranked_staff = [
        {"id": r.id, "name": r.name, "position": r.position, "count": r.shift_count}
        for r in ranking_data
    ]

    # 4. Gaps for selected month
    assigned_dates = (
        db.query(Schedule.duty_date)
        .filter(Schedule.duty_date.between(month_start, month_end))
        .distinct()
        .all()
    )
    unfilled_gaps = num_days - len(assigned_dates)

    return {
        "total_staff": db.query(Staff).count(),
        "today_shifts_count": today_shifts,
        "unfilled_gaps": unfilled_gaps,
        "ranked_staff": ranked_staff,
        "active_month_name": calendar.month_name[month]
    }
    today = date.today()
    
    # 1. Total workforce count
    total_staff = db.query(Staff).count()
    
    # 2. Today's assignments
    today_shifts = db.query(Schedule).filter(Schedule.duty_date == today).count()
    
    # 3. Personnel Utilization (FIXED TO INCLUDE 0 SHIFTS)
    # We use .outerjoin() to ensure staff with no schedules are still returned
    ranking_data = (
        db.query(
            Staff.id,
            Staff.name,
            Staff.position,
            func.count(Schedule.id).label("shift_count")
        )
        .outerjoin(Schedule, Staff.id == Schedule.staff_id) # Changed from .join()
        .group_by(Staff.id)
        .order_by(func.count(Schedule.id).desc(), Staff.name.asc()) # Secondary sort by name
        .limit(10) 
        .all()
    )
    
    ranked_staff = [
        {"id": r.id, "name": r.name, "position": r.position, "count": r.shift_count}
        for r in ranking_data
    ]

    # 4. Calculate Unfilled Days (Gaps) for current month
    _, num_days = calendar.monthrange(today.year, today.month)
    month_start = today.replace(day=1)
    month_end = today.replace(day=num_days)
    
    assigned_dates = (
        db.query(Schedule.duty_date)
        .filter(Schedule.duty_date.between(month_start, month_end))
        .distinct()
        .all()
    )
    assigned_set = {d[0] for d in assigned_dates}
    unfilled_gaps = num_days - len(assigned_set)

    return {
        "total_staff": total_staff,
        "today_shifts_count": today_shifts,
        "unfilled_gaps": unfilled_gaps,
        "ranked_staff": ranked_staff
    }
    today = date.today()
    
    total_staff = db.query(Staff).count()
    
    today_shifts = db.query(Schedule).filter(Schedule.duty_date == today).count()
    
    # SELECT staff_id, count(*) FROM schedules GROUP BY staff_id
    ranking_data = (
        db.query(
            Staff.id,
            Staff.name,
            Staff.position,
            func.count(Schedule.id).label("shift_count")
        )
        .join(Schedule, Staff.id == Schedule.staff_id)
        .group_by(Staff.id)
        .order_by(func.count(Schedule.id).desc())
        .limit(10) # Top 10 for dashboard performance
        .all()
    )
    
    ranked_staff = [
        {"id": r.id, "name": r.name, "position": r.position, "count": r.shift_count}
        for r in ranking_data
    ]

    # 4. Calculate Unfilled Days (Gaps) for current month
    _, num_days = calendar.monthrange(today.year, today.month)
    month_start = today.replace(day=1)
    month_end = today.replace(day=num_days)
    
    # Get all dates that have at least one assignment
    assigned_dates = (
        db.query(Schedule.duty_date)
        .filter(Schedule.duty_date.between(month_start, month_end))
        .distinct()
        .all()
    )
    assigned_set = {d[0] for d in assigned_dates}
    unfilled_gaps = num_days - len(assigned_set)

    return {
        "total_staff": total_staff,
        "today_shifts_count": today_shifts,
        "unfilled_gaps": unfilled_gaps,
        "ranked_staff": ranked_staff
    }