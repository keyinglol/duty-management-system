from pydantic import BaseModel, ConfigDict

class StaffCreate(BaseModel):
    name: str
    age: int
    position: str

class StaffResponse(BaseModel):
    id: int
    name: str
    age: int
    position: str

    model_config = ConfigDict(from_attributes=True)
