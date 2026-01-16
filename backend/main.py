from fastapi import FastAPI
from database import Base, engine
from database import engine
from routers import staff, schedule, statistics
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Duty Management System")


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],   # VERY IMPORTANT
    allow_headers=["*"],
)

# Create tables in database
Base.metadata.create_all(bind=engine)

# Include API routers
app.include_router(staff.router)
app.include_router(schedule.router)
app.include_router(statistics.router)
