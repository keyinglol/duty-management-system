from pydantic import BaseModel, ConfigDict
from datetime import date
from .staff_schema import StaffResponse  # import the Staff schema

class ScheduleCreate(BaseModel):
    staff_id: int
    duty_date: date

class ScheduleResponse(BaseModel):
    id: int
    staff: StaffResponse
    duty_date: date

    model_config = ConfigDict(from_attributes=True)
