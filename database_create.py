import sqlite3

def create_tables():
    conn = sqlite3.connect('meal_tracker.db')
    c = conn.cursor()

    # Create Meals table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Meals (
            meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            cuisine_type TEXT,
            cooking_mode TEXT,
            cooking_time INTEGER,
            image_path TEXT
        )
    ''')

    # Create Ingredients table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Ingredients (
            ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity FLOAT,
            unit TEXT
        )
    ''')

    # Create Meal_Ingredients table (many-to-many relationship)
    c.execute('''
        CREATE TABLE IF NOT EXISTS Meal_Ingredients (
            meal_id INTEGER,
            ingredient_id INTEGER,
            FOREIGN KEY(meal_id) REFERENCES Meals(meal_id),
            FOREIGN KEY(ingredient_id) REFERENCES Ingredients(ingredient_id),
            PRIMARY KEY(meal_id, ingredient_id)
        )
    ''')

    # Create Directions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Directions (
            direction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER,
            step_number INTEGER,
            description TEXT NOT NULL,
            FOREIGN KEY(meal_id) REFERENCES Meals(meal_id),
            PRIMARY KEY(meal_id, step_number)
        )
    ''')

    # Create Ratings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Ratings (
            rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER,
            user_id TEXT,
            rating_score INTEGER CHECK(rating_score >= 1 AND rating_score <= 5),
            FOREIGN KEY(meal_id) REFERENCES Meals(meal_id)
        )
    ''')

    # Create Images table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER,
            path TEXT NOT NULL,
            FOREIGN KEY(meal_id) REFERENCES Meals(meal_id)
        )
    ''')

    # Create Meal_Log table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Meal_Log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER,
            user_id TEXT,
            date_eaten DATE,
            FOREIGN KEY(meal_id) REFERENCES Meals(meal_id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print('executed')