import random
from datetime import date, timedelta
from sqlalchemy.orm import Session
from models.staff_model import Staff
from models.schedule_model import Schedule

# ----------------------------------------------------------------             
# 1. RULE DEFINITIONS
# ----------------------------------------------------------------

def rule_fairness_score(staff_id, context):
    return context['current_counts'].get(staff_id, 0)

def rule_rest_constraint(staff_id, context):
    if staff_id in context['last_assignments']:
        return 1000
    return 0

def rule_random_factor(staff_id, context):
    return random.random()

# ----------------------------------------------------------------
# 2. THE CORE LOGIC
# ----------------------------------------------------------------

def auto_schedule_logic(db: Session, start_date: date, end_date: date):
    try:
        # 1. Fetch Staff
        staff_members = db.query(Staff).all()
        if not staff_members:
            return {"status": "error", "message": "No staff found in database."}

        # 2. Identify existing assignments to "Fill-in-the-blanks"
        existing_schedules = db.query(Schedule).filter(
            Schedule.duty_date >= start_date,
            Schedule.duty_date <= end_date
        ).all()

        current_counts = {s.id: 0 for s in staff_members}
        pre_assigned_dates = {}

        for s in existing_schedules:
            current_counts[s.staff_id] += 1
            pre_assigned_dates[s.duty_date] = s.staff_id

        # 3. Context Initialization
        context = {
            "current_counts": current_counts,
            "last_assignments": [] 
        }

        active_rules = [rule_fairness_score, rule_rest_constraint, rule_random_factor]
        current_date = start_date

        # 4. Main Scheduling Loop
        while current_date <= end_date:
            # Check if day is already taken (Manual Assignment)
            if current_date in pre_assigned_dates:
                context['last_assignments'] = [pre_assigned_dates[current_date]]
                current_date += timedelta(days=1)
                continue

            # Calculate weighted pool
            weighted_pool = []
            for staff in staff_members:
                total_weight = sum(rule(staff.id, context) for rule in active_rules)
                weighted_pool.append((staff, total_weight))

            # Sort and pick the lowest weight
            weighted_pool.sort(key=lambda x: x[1])
            chosen_staff = weighted_pool[0][0]

            # Create new record
            new_duty = Schedule(staff_id=chosen_staff.id, duty_date=current_date)
            db.add(new_duty)

            # Update context for the next day
            context['current_counts'][chosen_staff.id] += 1
            context['last_assignments'] = [chosen_staff.id]
            current_date += timedelta(days=1)

        # 5. Commit everything at once
        db.commit()
        return {"status": "success", "message": f"Schedule generated from {start_date} to {end_date}"}

    except Exception as e:
        # If any error occurs, undo all pending changes
        db.rollback()
        print(f"Error in auto_scheduling: {e}")
        return {"status": "error", "message": str(e)}