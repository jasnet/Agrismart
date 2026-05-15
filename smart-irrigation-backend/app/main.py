from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import fields, sensors, schedule
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables
    create_db_and_tables()
    yield
    # Shutdown logic if needed

app = FastAPI(title="Smart Irrigation API", lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fields.router)
app.include_router(sensors.router)
app.include_router(schedule.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Smart Irrigation Backend"}
