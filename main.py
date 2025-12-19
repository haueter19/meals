from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload, subqueryload
from sqlalchemy import Column, Integer, String, ForeignKey, Float, text, Table
import pandas as pd
# Import models and schemas
from models import Meal, Ingredient, Direction, LogEntry, Image
from schemas import MealCreate, MealResponse, IngredientResponse, DirectionResponse, LogEntryResponse, MealStats
from db_config import get_db
import requests
from typing import Optional
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (use specific domains in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Ensure the templates directory is correctly set relative to the main.py location
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name='images')



def get_meal_with_ingredients(meal_id: int, db: Session):
    return db.query(Meal).options(joinedload(Meal.ingredients)).filter(Meal.meal_id == meal_id).first()



#
@app.get('/test/{meal_id}', response_model=MealResponse)
async def test(meal_id: int, db: Session = Depends(get_db)):
    a = text(f"SELECT * FROM Meals WHERE meal_id={meal_id}")
    df = pd.DataFrame(db.execute(a))
    print(df)
    meals = db.query(Meal).filter(Meal.meal_id == meal_id).first()#db.query(Meal).first()
    print(meals.__dict__)
    return MealResponse.model_validate(meals.__dict__)



# Creates a new meal
@app.post("/meals/", response_model=MealResponse)
async def create_meal(meal: MealCreate, db: Session = Depends(get_db)):
    db_meal = Meal(
        name=meal.name,
        description=meal.description,
        cuisine_type=meal.cuisine_type,
        cooking_mode=meal.cooking_mode,
        cooking_ease=meal.cooking_ease,
        cooking_time=meal.cooking_time,
        image_path=meal.image_path,
    )
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)

    # Add ingredients (handling many-to-many)
    for ingredient in meal.ingredients:
        # Check if ingredient already exists
        db_ingredient = db.query(Ingredient).filter_by(name=ingredient.name).first()
        if not db_ingredient:
            db_ingredient = Ingredient(name=ingredient.name, quantity=ingredient.quantity, unit=ingredient.unit)
            db.add(db_ingredient)
            db.commit()  # Commit new ingredient to get its ID

        db_meal.ingredients.append(db_ingredient)  # Associate meal with ingredient


    for direction in meal.directions:
        db_direction = db.query(Direction).filter_by(step_number=direction.step_number, meal_id=db_meal.meal_id).first()

        if not db_direction:
            db_direction = Direction(
                step_number=direction.step_number,
                description=direction.description,
            )
            db_direction.meal = db_meal  # ✅ Associate with meal before commit
            db.add(db_direction)
            db.commit()

        db_meal.directions.append(db_direction)


    db.commit()
    db.refresh(db_meal)

    return db_meal


# Gets all meals
@app.get("/meals/", response_model=list[MealResponse])
async def read_meals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    meals = (
        db.query(Meal)
        .options(joinedload(Meal.ingredients), joinedload(Meal.directions))
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Stats from Meal Log Entries
    meal_stats = pd.DataFrame(db.execute(text("""
                                            SELECT 
                                                meal_id, min(date) first_meal_date, max(date) recent_meal_date, count(meal_id) meal_count, avg(rating) avg_rating 
                                            FROM LogEntries
                                            WHERE meal_id IS NOT NULL
                                            GROUP BY meal_id
                                            LIMIT :limit 
                                            OFFSET :offset
                                            """), {'offset':skip, 'limit':limit}).all()
                                            )
    if meal_stats.shape[0] > 0:
        meal_stats = meal_stats.to_dict(orient='records')
    else:
        meal_stats = []

    print(meal_stats)
    meal_stats_list = []
    for row in meal_stats:
        meal_stats_list.append(
            MealStats(
                meal_id = int(row['meal_id']),
                first_meal_date=row['first_meal_date'],
                recent_meal_date=row['recent_meal_date'],
                meal_count=row['meal_count'],
                avg_rating=row['avg_rating']
            )
        )
    print(meal_stats_list)
    return [
        MealResponse(
            meal_id=meal.meal_id,
            name=meal.name,
            description=meal.description,
            cuisine_type=meal.cuisine_type,
            cooking_mode=meal.cooking_mode,
            cooking_ease=meal.cooking_ease,
            cooking_time=meal.cooking_time,
            image_path=meal.image_path,
            ingredients=[
                IngredientResponse.model_validate(ing.__dict__) for ing in meal.ingredients
            ],
            directions=[
                DirectionResponse.model_validate(dir.__dict__) for dir in meal.directions
            ], log_entries=[
                LogEntryResponse.model_validate(ent.__dict__) for ent in meal.log_entries
            ], meal_stats=[MealStats.model_validate(m.__dict__) for m in meal_stats_list if m.meal_id == meal.meal_id]
        )
        for meal in meals
    ]




# Changes a single meal
@app.put("/meals/{meal_id}", response_model=MealResponse)
async def update_meal(meal_id: int, meal_update: MealCreate, db: Session = Depends(get_db)):
    db_meal = db.query(Meal).filter(Meal.meal_id == meal_id).first()

    if db_meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    # Convert Pydantic model to dict
    update_data = meal_update.model_dump()
    #print(update_data)

    # ✅ Only update valid attributes
    for key, value in update_data.items():
        if hasattr(db_meal, key) and not isinstance(value, list): # This process cannot properly handle relationships
            setattr(db_meal, key, value)
        #else:
            #print(f"Skipping unknown attribute: {key}")  # Debugging

    # ✅ Clear and replace ingredients
    if "ingredients" in update_data:
        db_meal.ingredients.clear()  # Remove old ingredients
        for ingredient_data in update_data["ingredients"]:
            ingredient = db.query(Ingredient).filter_by(name=ingredient_data["name"]).first()
            if not ingredient:
                ingredient = Ingredient(**ingredient_data)  # Create new if not found
                db.add(ingredient)
            db_meal.ingredients.append(ingredient)  # Add to meal

    if "directions" in update_data:
        # ❌ Don't use .clear()—this causes the blanking issue!
        db.query(Direction).filter(Direction.meal_id == db_meal.meal_id).delete()  # Delete old directions
        
        for direction_data in update_data["directions"]:
            new_direction = Direction(
                meal_id=db_meal.meal_id,  # ✅ Ensure foreign key is set
                step_number=direction_data["step_number"],
                description=direction_data["description"]
            )
            db.add(new_direction)  # Add new direction

    if "log_entries" in update_data:
        # ❌ Don't use .clear()—this causes the blanking issue!
        db.query(LogEntry).filter(LogEntry.meal_id == db_meal.meal_id).delete()  # Delete old directions
        
        for entry in update_data["log_entries"]:
            new_entry = LogEntry(
                meal_id=db_meal.meal_id,  # ✅ Ensure foreign key is set
                date=entry["date"],
                rating=entry["rating"],
                notes=entry['notes']
            )
            db.add(new_entry)  # Add new direction

    db.commit()
    db.refresh(db_meal)

    return db_meal


# Deletes a single meal
@app.delete("/meals/{meal_id}", response_model=dict)
async def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.meal_id == meal_id).first()
    if meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    
    db.delete(meal)
    db.commit()
    return {"detail": "Meal deleted"}


# Redirect to meals
@app.get('/', response_class=RedirectResponse)
async def gotoentry(request:Request):
    return RedirectResponse('/find')



# Returns the meal entry form web page
@app.get('/find', response_class=HTMLResponse)
async def meal_entry_form(request:Request):
    return templates.TemplateResponse('meal_finder.html', {'request':request})



# Returns the meal entry form web page
@app.get('/meal/{meal_id}', response_class=HTMLResponse)
async def meal_entry_form(request: Request, meal_id: int, db: Session = Depends(get_db)):
    meal = (
        db.query(Meal)
        .options(
            subqueryload(Meal.ingredients),  # ✅ Fix: Use subqueryload for Many-to-Many
            joinedload(Meal.directions),  # ✅ Works fine for One-to-Many
            joinedload(Meal.log_entries)
        )
        .filter(Meal.meal_id == meal_id)
        .first()
    )
    # Stats from Meal Log Entries
    meal_stats = pd.DataFrame(db.execute(text("""
                                                SELECT 
                                                    meal_id, min(date) first_meal_date, max(date) recent_meal_date, count(meal_id) meal_count, avg(rating) avg_rating 
                                                FROM LogEntries 
                                                WHERE 
                                                    meal_id=:meal_id GROUP BY meal_id"""), {'meal_id':meal_id}).all())
    if meal_stats.shape[0] > 0:
        meal_stats = meal_stats.set_index('meal_id').to_dict(orient='index')
    else:
        meal_stats = {meal_id:{'first_meal_date':'never', 'recent_meal_date':'never', 'meal_count':0, 'avg_rating':0}}

    if not meal:
        return HTMLResponse(content="Meal not found", status_code=404)
    
    meal_data = {
        "meal_id": meal.meal_id,
        "name": meal.name,
        "description": meal.description,
        "cuisine_type": meal.cuisine_type,
        "cooking_mode": meal.cooking_mode,
        "cooking_ease": meal.cooking_ease,
        "cooking_time": meal.cooking_time,
        "image_path": meal.image_path,
        "ingredients": [
            {"ingredient_id": ing.ingredient_id, "name": ing.name, "quantity": ing.quantity, "unit": ing.unit}
            for ing in meal.ingredients
        ],
        "directions": [
            {"step_number": dir.step_number, "description": dir.description}
            for dir in meal.directions
        ],
        "logEntries": [
            {"date": log_entry.date, "rating":log_entry.rating, "notes":log_entry.notes}
            for log_entry in meal.log_entries
        ],
        "mealStats": meal_stats[meal_id],
    }

    return templates.TemplateResponse('meal_entry_form.html', {'request': request, 'meal': meal_data})




# Returns the meal entry form web page
@app.get('/entry', response_class=HTMLResponse)
async def meal_entry_form(request:Request):
    return templates.TemplateResponse('meal_entry_form.html', {'request':request, 'meal':{'meal_id':-1}})



# Endpoint to handle image upload
@app.post("/meals/{meal_id}/upload-image/")
async def upload_image(meal_id: int, image: UploadFile = File(...), db: Session = Depends(get_db)):
    # Define the directory to save uploaded images
    if image:
        # Define the directory to save uploaded images
        upload_directory = "assets/images"
        os.makedirs(upload_directory, exist_ok=True)

        # Save the uploaded file
        file_location = f"{upload_directory}/{image.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Create a new Image record in the database
        new_image = Image(meal_id=meal_id, path=file_location)
        db.add(new_image)
        db.commit()
        db.refresh(new_image)

        return {"message": "Image uploaded successfully", "image_id": new_image.image_id}
    else:
        return {"message": "Image upload unsuccessful"}