# Punto de entrada de la aplicación FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import fish, plants, maintenance, acuario, lighting
from app.routers import auth as auth_router

app = FastAPI(
    title="Acuarium Management API",
    version="2.0.0",
    description="API REST para la gestión de un acuario con autenticación JWT.",
    swagger_ui_init_oauth={},
    # Configura el botón Authorize de Swagger con Bearer JWT
    swagger_ui_parameters={"persistAuthorization": True},
    openapi_tags=[
        {"name": "auth",        "description": "Autenticación y gestión de usuarios"},
        {"name": "acuario",     "description": "Gestión de acuarios"},
        {"name": "fish",        "description": "Gestión de peces"},
        {"name": "plants",      "description": "Gestión de plantas"},
        {"name": "lighting",    "description": "Gestión de iluminación"},
        {"name": "maintenance", "description": "Tareas de mantenimiento"},
    ],
)

# Permitir peticiones desde el frontend Vue durante desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seguridad global en el schema OpenAPI (muestra el candado en Swagger)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    from fastapi.openapi.utils import get_openapi
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema.setdefault("components", {}).setdefault("securitySchemes", {})["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    # Aplicar seguridad global a todos los endpoints (excepto los que ya tienen security:[])
    for path_data in schema.get("paths", {}).values():
        for operation in path_data.values():
            if isinstance(operation, dict) and "security" not in operation:
                operation["security"] = [{"bearerAuth": []}]
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi  # type: ignore[method-assign]

# Routers
app.include_router(auth_router.router)
app.include_router(fish.router)
app.include_router(plants.router)
app.include_router(maintenance.router)
app.include_router(acuario.router)
app.include_router(lighting.router)
