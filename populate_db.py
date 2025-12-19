from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base, Meal, Ingredient, Direction, Rating, Image, LogEntry

DATABASE_URL = "sqlite:///data/meal_tracker.db"
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
            cooking_ease="medium",
            cooking_time=30,
            image_path="image.jpg"
        )

        meal2 = Meal(
            name="Chicken Alfredo",
            description="Creamy pasta dish with chicken in a parmesan sauce.",
            cuisine_type="Italian",
            cooking_mode="stove",
            cooking_ease="easy",
            cooking_time=45,
            image_path="image.jpg"
        )

        meal3 = Meal(
            name="Beef Tacos",
            description="Seasoned ground beef in crispy taco shells with fresh toppings.",
            cuisine_type="Mexican",
            cooking_mode="stove",
            cooking_ease="easy",
            cooking_time=20,
            image_path="image.jpg"
        )

        meal4 = Meal(
            name="Grilled Salmon",
            description="Fresh salmon fillet grilled to perfection with lemon and herbs.",
            cuisine_type="American",
            cooking_mode="grill",
            cooking_ease="medium",
            cooking_time=25,
            image_path="image.jpg"
        )

        meal5 = Meal(
            name="Vegetable Stir Fry",
            description="Quick and healthy stir-fried vegetables with soy sauce and ginger.",
            cuisine_type="Asian",
            cooking_mode="stove",
            cooking_ease="easy",
            cooking_time=15,
            image_path="image.jpg"
        )

        # Add meals to the database
        db.add_all([meal1, meal2, meal3, meal4, meal5])
        db.commit()

        # Create some sample ingredients
        ing1 = Ingredient(name="Spaghetti", quantity=400, unit="grams")
        ing2 = Ingredient(name="Pancetta", quantity=150, unit="grams")
        ing3 = Ingredient(name="Eggs", quantity=4, unit="whole")
        ing4 = Ingredient(name="Parmesan Cheese", quantity=100, unit="grams")
        ing5 = Ingredient(name="Chicken Breast", quantity=500, unit="grams")
        ing6 = Ingredient(name="Heavy Cream", quantity=250, unit="ml")
        ing7 = Ingredient(name="Ground Beef", quantity=500, unit="grams")
        ing8 = Ingredient(name="Taco Shells", quantity=12, unit="pieces")
        ing9 = Ingredient(name="Salmon Fillet", quantity=600, unit="grams")
        ing10 = Ingredient(name="Mixed Vegetables", quantity=500, unit="grams")
        ing11 = Ingredient(name="Soy Sauce", quantity=3, unit="tbsp")

        db.add_all([ing1, ing2, ing3, ing4, ing5, ing6, ing7, ing8, ing9, ing10, ing11])
        db.commit()

        # Associate ingredients with meals
        meal1.ingredients.extend([ing1, ing2, ing3, ing4])
        meal2.ingredients.extend([ing1, ing5, ing6, ing4])
        meal3.ingredients.extend([ing7, ing8])
        meal4.ingredients.append(ing9)
        meal5.ingredients.extend([ing10, ing11])

        db.commit()

        # Create sample directions
        Direction(meal=meal1, step_number=1, description="Bring a large pot of salted water to boil and cook spaghetti according to package directions.")
        Direction(meal=meal1, step_number=2, description="In a bowl, whisk together eggs and grated Parmesan cheese.")
        Direction(meal=meal1, step_number=3, description="Cook pancetta in a large pan until crispy.")
        Direction(meal=meal1, step_number=4, description="Drain pasta and toss with pancetta, then remove from heat and stir in egg mixture.")

        Direction(meal=meal2, step_number=1, description="Cook pasta according to package directions.")
        Direction(meal=meal2, step_number=2, description="Season and cook chicken until golden and cooked through.")
        Direction(meal=meal2, step_number=3, description="Add cream and Parmesan to the pan and simmer until thickened.")
        Direction(meal=meal2, step_number=4, description="Toss cooked pasta with the sauce and sliced chicken.")

        Direction(meal=meal3, step_number=1, description="Brown ground beef in a skillet and season with taco seasoning.")
        Direction(meal=meal3, step_number=2, description="Warm taco shells according to package directions.")
        Direction(meal=meal3, step_number=3, description="Fill shells with beef and your favorite toppings.")

        Direction(meal=meal4, step_number=1, description="Preheat grill to medium-high heat.")
        Direction(meal=meal4, step_number=2, description="Season salmon with salt, pepper, and lemon juice.")
        Direction(meal=meal4, step_number=3, description="Grill salmon skin-side down for 6-8 minutes, flip and cook another 3-4 minutes.")

        Direction(meal=meal5, step_number=1, description="Heat oil in a wok or large skillet over high heat.")
        Direction(meal=meal5, step_number=2, description="Add vegetables and stir-fry for 5-7 minutes.")
        Direction(meal=meal5, step_number=3, description="Add soy sauce and toss to coat. Serve hot.")

        db.commit()

        # Add log entries
        LogEntry(meal=meal1, date="2024-12-01", rating=5, notes="Delicious! Made for dinner.")
        LogEntry(meal=meal1, date="2024-11-15", rating=5, notes="Family favorite.")
        LogEntry(meal=meal2, date="2024-12-10", rating=4, notes="Good but a bit heavy.")
        LogEntry(meal=meal3, date="2024-12-05", rating=5, notes="Quick and tasty!")
        LogEntry(meal=meal3, date="2024-11-20", rating=4, notes="Kids loved it.")
        LogEntry(meal=meal4, date="2024-12-08", rating=5, notes="Perfectly cooked salmon.")
        LogEntry(meal=meal5, date="2024-12-12", rating=4, notes="Healthy and quick weeknight meal.")

        db.commit()

        print("✅ Successfully added 5 sample meals to the database!")

    finally:
        db.close()

if __name__ == "__main__":
    populate_db()