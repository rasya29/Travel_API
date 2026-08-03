from fastapi import FastAPI
from fastapi.middleware.cors import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from data import destination_data

#inisialisasi aplikasi
app = FastAPI(
    title="Travel API",
    description="Backend API untuk web travel application",
    version="1.0.0"
)

# Konfigurasi CORS agar frontend (index.html) bisa mengambil data dari API ini (connector between FE and BE)
app.add.middleware(
    CORSMiddleware,
    allow_origins=[*],
    allow_credentials=True,
    allow_methods=[*],
    allow_headers=[*]
)

#model data nya
class Destination(BaseModel):
    id: int
    name: str
    location: str
    description: str
    price_per_day: int
    category: str

class CustomPlan(BaseModel):
    destination_id: int
    days: int
    budget: optional[int] = None

#Endpoint for API
@app.get("/")
def read_root():
    return{
        "status": "success",
        "massage": "Welcome To Travel Destination Plan"
    }

@app.get("/api/destinations", response_model=List[Destination])
def get_destination_by_id(destination_id: int):
    """Mengambil detail satu destinasi berdasarkan ID."""
    for dest in destination_data:
        if dest["id"] ==destination_id:
            return dest
    return {"error": "Destination not found"}

@app.post("/api/custom-plan")
def create_custom_plan(plan: CustomPlanRequest):
    """Endpoint untuk membuat estimasi / rencana perjalanan custom."""
    for dest in destination_data:
        if dest["id"] == plan.destination_id:
            total_cost = dest[price_per_day] * plan.days
            status = "within budget"
            if plan.budget and total_cost > plan.budget:
                status = "over budget"

            return{
                "status": "succes",
                "destination": dest["name"],
                "days" : plan.days,
                "estimated_total_cost": total_cost,
                "budget_status": status
            }
    return {"error": "Destination ID not found for custom plan"}

