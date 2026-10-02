from typing import List, Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=150)
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: str
    password: str


class HomePlannerRequest(BaseModel):
    room_type: str
    room_size: str
    budget: float = Field(gt=0)
    style: str
    colors: Optional[str] = ""
    requirements: Optional[str] = ""


class PartyPlannerRequest(BaseModel):
    event_type: str
    guests: int = Field(gt=0)
    budget: float = Field(gt=0)
    venue: str
    theme: str
    food_preference: Optional[str] = ""
    requirements: Optional[str] = ""


class JewelryPlannerRequest(BaseModel):
    occasion: str
    outfit: str
    metal: str
    budget: float = Field(gt=0)
    style: str
    requirements: Optional[str] = ""


class RecommendationItem(BaseModel):
    name: str
    description: str
    estimated_price: Optional[str] = None
    reason: Optional[str] = None
    tips: Optional[List[str]] = None


class RecommendationResponse(BaseModel):
    title: str
    summary: str
    recommendations: List[RecommendationItem]
    budget_note: Optional[str] = None