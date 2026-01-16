from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.statistics_service import get_dashboard_summary

router = APIRouter(prefix="/statistics", tags=["statistics"])

@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    """
    Returns aggregated data for the admin dashboard.
    Includes staff counts, today's workload, and ranked personnel.
    """
    return get_dashboard_summary(db)