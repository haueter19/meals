# Meals Tracker

A FastAPI-based web application for tracking meals, ingredients, recipes, and meal logs.

## Features

- Browse and search meals
- Add new meals with ingredients and directions
- Log meal entries with ratings and notes
- Upload meal images
- View meal statistics

## Running with Docker

### Prerequisites

- Docker and Docker Compose installed on your system
- The application will be accessible on port 8000

### Quick Start

1. Build and start the container:
```bash
docker compose up -d
```

2. Access the application:
   - From the host machine: `http://localhost:8000`
   - From other devices on your local network: `http://YOUR_PI_IP:8000`
     (Replace `YOUR_PI_IP` with your Raspberry Pi's IP address, e.g., `http://192.168.1.100:8000`)

3. To find your Raspberry Pi's IP address:
```bash
hostname -I
```

### Docker Commands

- **Start the application**: `docker compose up -d`
- **Stop the application**: `docker compose down`
- **View logs**: `docker compose logs -f`
- **Rebuild after changes**: `docker compose up -d --build`

### Data Persistence

The following data is persisted using Docker volumes:
- SQLite database - Stored in a named Docker volume `meal_data` (located at `/app/data/meal_tracker.db` inside container)
- Uploaded meal images - Bind-mounted from host `assets/` directory

**Accessing the database:**
```bash
# View volume information
docker volume inspect meals_meal_data

# Backup the database
docker compose exec meals-app cp /app/data/meal_tracker.db /app/assets/meal_tracker_backup.db
# Then find it in your local assets/ directory

# Reset the database (removes all data)
docker compose down
docker volume rm meals_meal_data
docker compose up -d
```

## Running Locally (without Docker)

1. Install dependencies:
```bash
pip install uv
uv pip install -r pyproject.toml
```

2. Run the application:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Project Structure

- `main.py` - FastAPI application and routes
- `models.py` - SQLAlchemy database models
- `schemas.py` - Pydantic schemas for API validation
- `db_config.py` - Database configuration
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript)
- `assets/` - Uploaded images
- `meal_tracker.db` - SQLite database
