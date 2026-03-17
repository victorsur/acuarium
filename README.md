# Acuarium 🐠

SDD (Spec-Driven Development) example project built with **FastAPI**, **MySQL**, and **Vue 3**. Architected by me and generated via AI.

An aquarium management and maintenance tool that tracks aquarium types, maintenance tasks, lighting, fish, and plants.

## Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Backend   | FastAPI + SQLAlchemy 2  |
| Database  | MySQL 8.0               |
| Frontend  | Vue 3 + Vite            |
| Container | Docker + Docker Compose |

## Features

- 🏠 **Dashboard** — overview with counts of aquariums, fish, plants, and pending tasks
- 📋 **Aquarium Types** — manage types (freshwater, marine, brackish, etc.)
- 🐠 **Aquariums** — CRUD for individual aquariums with volume and setup date
- 🐟 **Fish** — track fish species and quantities per aquarium
- 🌿 **Plants** — track plant species and quantities per aquarium
- 💡 **Lighting** — schedule daily on/off times and intensity per aquarium
- 🔧 **Maintenance Tasks** — schedule and track water changes, filter cleans, etc.

## Getting Started

### Prerequisites
- Docker & Docker Compose

### Run with Docker Compose

```bash
# Copy environment file
cp .env.example .env

# Start all services
docker compose up --build
```

The application will be available at:
- **Frontend**: http://localhost:80
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
acuarium/
├── backend/            # FastAPI application
│   ├── app/
│   │   ├── models/     # SQLAlchemy ORM models
│   │   ├── schemas/    # Pydantic request/response schemas
│   │   ├── routers/    # API route handlers
│   │   ├── config.py   # Application settings
│   │   ├── database.py # DB connection & session
│   │   └── main.py     # FastAPI app entry point
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/           # Vue 3 application
│   ├── src/
│   │   ├── api/        # Axios API client
│   │   ├── router/     # Vue Router routes
│   │   └── views/      # Page components
│   ├── package.json
│   └── Dockerfile
├── db/
│   └── init.sql        # Database initialization
├── docker-compose.yml
└── .env.example
```

## API Endpoints

| Method | Path                           | Description              |
|--------|--------------------------------|--------------------------|
| GET    | /api/aquarium-types            | List aquarium types      |
| POST   | /api/aquarium-types            | Create aquarium type     |
| GET    | /api/aquariums                 | List aquariums           |
| POST   | /api/aquariums                 | Create aquarium          |
| GET    | /api/aquariums/{id}            | Get aquarium detail      |
| GET    | /api/fish                      | List fish                |
| GET    | /api/plants                    | List plants              |
| GET    | /api/lighting                  | List lighting schedules  |
| GET    | /api/maintenance-tasks         | List maintenance tasks   |
| PATCH  | /api/maintenance-tasks/{id}/complete | Mark task complete |

Full interactive API documentation: `http://localhost:8000/docs`
