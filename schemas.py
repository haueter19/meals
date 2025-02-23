from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Union, List

# Define Pydantic models for request/response bodies



class IngredientResponse(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None

    class Config:
        orm_mode = True

class DirectionResponse(BaseModel):
    step_number: int
    description: str

    class Config:
        orm_mode = True


class LogEntryResponse(BaseModel):
    date: str
    rating: Optional[int] = -1
    notes: Optional[str] = None

    class Config:
        orm_mode = True

class MealStats(BaseModel):
    meal_id: int
    first_meal_date: Optional[str] = None
    recent_meal_date: Optional[str] = None
    meal_count: Optional[int] = 0
    avg_rating: Optional[float] = 0.0


class MealCreate(BaseModel):
    name: str
    description: str
    cuisine_type: Optional[str] = None
    cooking_mode: Optional[str] = None
    cooking_ease: Optional[str] = None
    cooking_time: Optional[int] = None
    image_path: Optional[str] = None  # Optional field
    ingredients: Optional[List[IngredientResponse]] = []
    directions: Optional[List[DirectionResponse]] = []
    log_entries: Optional[List[LogEntryResponse]] = []


class MealResponse(BaseModel):
    meal_id: int
    name: str
    description: str
    cuisine_type: Optional[str] = None
    cooking_mode: Optional[str] = None
    cooking_ease: Optional[str] = None
    cooking_time: Optional[int] = None
    image_path: Optional[str] = None
    ingredients: List[IngredientResponse] = []
    directions: List[DirectionResponse] = []
    log_entries: List[LogEntryResponse] = []
    meal_stats: List[MealStats] = []
    
    class Config:
        orm_mode = True

