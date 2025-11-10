from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from database import db, create_document, get_documents
import os

app = FastAPI(title="H2H Gym – King Mariout API", version="1.0.0")

# CORS for the frontend
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TrialBooking(BaseModel):
    name: str = Field(..., min_length=2, description="Full name")
    email: Optional[EmailStr] = None
    phone: str = Field(..., min_length=6, description="Contact phone or WhatsApp")
    goal: Optional[str] = Field(None, description="Fitness goal or notes")
    source: Optional[str] = Field("website", description="Lead source")


@app.get("/")
async def root():
    return {"message": "H2H Gym – King Mariout API running"}


@app.get("/test")
async def test():
    try:
        # Simple ping to DB
        collections = db.list_collection_names() if db else []
        return {
            "backend": "ok",
            "database": "ok" if db else "not-configured",
            "database_url": bool(os.getenv("DATABASE_URL")),
            "database_name": os.getenv("DATABASE_NAME"),
            "connection_status": "connected" if db else "missing env",
            "collections": collections,
        }
    except Exception as e:
        return {
            "backend": "ok",
            "database": "error",
            "connection_status": f"error: {e}",
        }


@app.post("/trial")
async def create_trial(booking: TrialBooking):
    try:
        payload = booking.model_dump()
        payload["received_at"] = datetime.utcnow().isoformat()
        inserted_id = create_document("trialbooking", payload)
        return {"status": "success", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
