from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Meal, Ingredient, Direction, Rating, Image, LogEntry

DATABASE_URL = "sqlite:///meal_tracker.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def populate_db():
    db: Session = SessionLocal()
    
    try:
        # Create some sample meals
        meal1 = Meal(
            name="Spaghetti Carbonara",
            description="A classic Italian pasta dish made with eggs, cheese, and pancetta.",
            cuisine_type="Italian",
            cooking_mode="stove",
            cooking_time=30,
            image_path="spaghetti_carbonara.jpg"
        )
        
        meal2 = Meal(
            name="Chicken Alfredo",
            description="Creamy pasta dish with chicken in a parmesan sauce.",
            cuisine_type="Italian",
            cooking_mode="oven",
            cooking_time=45,
            image_path="chicken_alfredo.jpg"
        )

        # Add meals to the database
        db.add_all([meal1, meal2])
        db.commit()

        # Create some sample ingredients for each meal
        ingredient1 = Ingredient(name="Spaghetti", quantity=200, unit="grams")
        ingredient2 = Ingredient(name="Pancetta", quantity=50, unit="grams")
        ingredient3 = Ingredient(name="Eggs", quantity=4, unit="")
        ingredient4 = Ingredient(name="Parmesan Cheese", quantity=100, unit="grams")

        db.add_all([ingredient1, ingredient2, ingredient3, ingredient4])
        db.commit()

        # Associate ingredients with meals
        meal1.ingredients.append(ingredient1)
        meal1.ingredients.append(ingredient2)
        meal1.ingredients.append(ingredient3)
        meal1.ingredients.append(ingredient4)

        meal2.ingredients.append(ingredient1)
        meal2.ingredients.append(ingredient3)

        db.commit()

        # Create some sample directions for each meal
        direction1 = Direction(meal=meal1, step_number=1, description="Cook spaghetti in boiling water.")
        direction2 = Direction(meal=meal1, step_number=2, description="Mix eggs and cheese.")
        direction3 = Direction(meal=meal1, step_number=3, description="Combine cooked pasta with egg mixture.")

        db.add_all([direction1, direction2, direction3])
        db.commit()

        # Add ratings for each meal
        rating1 = Rating(meal=meal1, user_id=1, rating=4.5)
        rating2 = Rating(meal=meal2, user_id=1, rating=4.0)

        db.add_all([rating1, rating2])
        db.commit()

        # Add images for each meal
        image1 = Image(meal=meal1, image_path="spaghetti_carbonara.jpg")
        image2 = Image(meal=meal2, image_path="chicken_alfredo.jpg")

        db.add_all([image1, image2])
        db.commit()

        # Add log entries for each meal
        log_entry1 = LogEntry(meal=meal1, timestamp="2023-10-05 14:30", notes="First recorded meal.")
        log_entry2 = LogEntry(meal=meal2, timestamp="2023-10-06 18:00", notes="Second recorded meal.")

        db.add_all([log_entry1, log_entry2])
        db.commit()

    finally:
        db.close()

if __name__ == "__main__":
    populate_db()