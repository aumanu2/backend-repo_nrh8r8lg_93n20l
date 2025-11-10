from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Each model -> collection name lowercased

class Trainer(BaseModel):
    name: str = Field(..., description="Trainer full name")
    specialty: str = Field(..., description="Primary specialty e.g., Strength, CrossFit, Boxing")
    bio: Optional[str] = Field(None, description="Short bio")
    photo_url: Optional[str] = Field(None, description="Photo URL")
    instagram: Optional[str] = None

class Program(BaseModel):
    title: str = Field(..., description="Program name")
    description: str = Field(..., description="What it includes")
    level: str = Field(..., description="Beginner / Intermediate / Advanced")
    icon: Optional[str] = Field(None, description="Icon keyword for UI")

class Membership(BaseModel):
    name: str
    price_month: Optional[float] = None
    price_year: Optional[float] = None
    benefits: List[str] = []

class Testimonial(BaseModel):
    name: str
    quote: str
    image_url: Optional[str] = None
    transformation_before: Optional[str] = None
    transformation_after: Optional[str] = None

class TrialBooking(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: str
    goal: Optional[str] = None
    source: Optional[str] = "website"
