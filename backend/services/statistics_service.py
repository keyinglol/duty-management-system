import calendar  
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.staff_model import Staff
from models.schedule_model import Schedule

def get_dashboard_summary(db: Session):
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