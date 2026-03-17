from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import aquarium_types, aquariums, fish, lighting, maintenance_tasks, plants

app = FastAPI(
    title="Acuarium API",
    description="Aquarium management backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(aquarium_types.router, prefix=settings.API_PREFIX)
app.include_router(aquariums.router, prefix=settings.API_PREFIX)
app.include_router(fish.router, prefix=settings.API_PREFIX)
app.include_router(plants.router, prefix=settings.API_PREFIX)
app.include_router(lighting.router, prefix=settings.API_PREFIX)
app.include_router(maintenance_tasks.router, prefix=settings.API_PREFIX)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


@app.get("/", tags=["Root"])
def root():
    return {"message": "Acuarium API", "docs": "/docs"}
