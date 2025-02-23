from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define association tables for many-to-many relationships
meal_ingredients_association_table = Table('Meal_Ingredients', Base.metadata,
    Column('meal_id', Integer, ForeignKey('Meals.meal_id')),
    Column('ingredient_id', Integer, ForeignKey('Ingredients.ingredient_id'))
)

class Meal(Base):
    __tablename__ = 'Meals'
    
    meal_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text)
    cuisine_type = Column(String(50))
    cooking_mode = Column(String(50))  # e.g., stove, oven
    cooking_ease = Column(String(50))
    cooking_time = Column(Integer)      # in minutes
    image_path = Column(String)
    source_url = Column(String)

    ingredients = relationship("Ingredient", secondary=meal_ingredients_association_table, back_populates="meals")
    directions = relationship("Direction", back_populates="meal", cascade="all, delete-orphan")

    ratings = relationship("Rating", backref="meal")
    images = relationship("Image", backref="meal")
    log_entries = relationship("LogEntry", backref="meal")


class Ingredient(Base):
    __tablename__ = 'Ingredients'

    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    quantity = Column(Float)
    unit = Column(String(50))

    meals = relationship("Meal", secondary=meal_ingredients_association_table, back_populates="ingredients")


class Direction(Base):
    __tablename__ = 'Directions'

    meal_id = Column(Integer, ForeignKey('Meals.meal_id'), primary_key=True)
    step_number = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False)

    meal = relationship("Meal", back_populates="directions")

class Rating(Base):
    __tablename__ = 'Ratings'

    rating_id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey('Meals.meal_id'))
    rating = Column(Integer)
    # Other rating fields

class Image(Base):
    __tablename__ = 'Images'

    image_id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey('Meals.meal_id'))
    path = Column(Text)
    # Other image fields

class LogEntry(Base):
    __tablename__ = 'LogEntries'

    log_entry_id = Column(Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey('Meals.meal_id'))
    date = Column(Text)
    rating = Column(Integer, nullable=True)
    notes = Column(Text)
    # Other log entry fields
