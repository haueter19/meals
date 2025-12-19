# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A FastAPI-based web application for tracking meals, ingredients, recipes, and meal logs. The application uses SQLAlchemy ORM with SQLite for data persistence and Jinja2 templates for server-side rendering.

## Running the Application

### Docker (Recommended)
```bash
# Build and start
docker compose up -d

# Stop
docker compose down

# Rebuild after changes
docker compose up -d --build

# View logs
docker compose logs -f
```

Application runs on port 8000. Access locally at `http://localhost:8000` or from network at `http://<PI_IP>:8000`.

### Local Development
```bash
# Install dependencies
pip install uv
uv pip install -r pyproject.toml

# Run server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Architecture

### Database Layer
- **ORM**: SQLAlchemy with declarative base models
- **Database**: SQLite (`meal_tracker.db`)
- **Session Management**: `db_config.py` provides `get_db()` dependency for FastAPI routes

### Data Models (`models.py`)
The application uses SQLAlchemy ORM models with the following relationships:

- **Meal** (primary entity)
  - Many-to-many with **Ingredient** via `Meal_Ingredients` association table
  - One-to-many with **Direction** (recipe steps)
  - One-to-many with **LogEntry** (meal history/logs)
  - One-to-many with **Rating**
  - One-to-many with **Image**

Key model relationships:
- Use `joinedload()` for one-to-many relationships (Directions, LogEntries)
- Use `subqueryload()` for many-to-many relationships (Ingredients) to avoid N+1 queries

### API Layer (`main.py`)
FastAPI application with:
- RESTful endpoints for CRUD operations on meals
- Hybrid approach: Returns JSON from `/meals/` endpoints AND server-rendered HTML from `/find`, `/meal/{id}`, `/entry`
- Pydantic schemas (`schemas.py`) for request/response validation
- CORS enabled for all origins (configured for development)

### Frontend
- Server-side rendered Jinja2 templates in `templates/`
- Static JavaScript in `static/js/` handles client-side interactivity
- Image uploads stored in `assets/images/`

## Key Implementation Patterns

### Querying Meals with Relationships
When fetching meals with their related data, always use appropriate eager loading:

```python
meal = (
    db.query(Meal)
    .options(
        subqueryload(Meal.ingredients),  # Many-to-many
        joinedload(Meal.directions),     # One-to-many
        joinedload(Meal.log_entries)     # One-to-many
    )
    .filter(Meal.meal_id == meal_id)
    .first()
)
```

### Updating Relationships
When updating meal directions or log entries (one-to-many with composite PKs):
- **Don't use `.clear()`** - causes issues with composite primary keys
- Instead, explicitly delete old records: `db.query(Direction).filter(Direction.meal_id == meal_id).delete()`
- Then create new records with proper foreign key assignment

See `update_meal()` endpoint in `main.py:166` for reference implementation.

### Meal Statistics
Meal statistics (first/last eaten, count, avg rating) are computed via raw SQL queries using `pd.DataFrame(db.execute(text(...)))` and joined with meal data. This pattern is used in both the `/meals/` list endpoint and individual meal views.

## Database Management

### Initialize Database
```bash
python database_create.py
```

### Populate with Sample Data
```bash
python populate_db.py
```

Note: `db_config.py` automatically creates tables via `Base.metadata.create_all()` on import, but utility scripts exist for manual setup.

## File Upload
Images are uploaded via `/meals/{meal_id}/upload-image/` endpoint and stored in `assets/images/`. The path is saved to the `Images` table with foreign key to the meal.

## Data Persistence (Docker)
Docker named volumes persist data across container restarts:
- `meal_data` volume - Mounted to `/app/data/` containing `meal_tracker.db`
- `assets/` directory - Bind-mounted for uploaded images

The database is stored at `data/meal_tracker.db` inside the container and persists in the `meal_data` Docker volume.
