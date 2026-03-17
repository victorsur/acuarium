# API REST Acuario: FastAPI + MySQL + Vue 3

> Proyecto de aprendizaje desarrollado siguiendo **SDD (Spec Driven Development)**: primero se define el contrato en `openapi.yaml` y todo el código — backend y frontend — se construye a partir de él.

---

## Tabla de Contenidos

- [Descripción](#descripción)
- [Arquitectura y stack](#arquitectura-y-stack)
- [Requisitos](#requisitos)
- [Estructura de carpetas](#estructura-de-carpetas)
- [Pasos seguidos en SDD](#pasos-seguidos-en-sdd)
- [Estado del proyecto (Roadmap SDD)](#estado-del-proyecto-roadmap-sdd)
- [Arranque rápido con Makefile](#arranque-rápido-con-makefile)
- [Arranque manual con Docker Compose](#arranque-manual-con-docker-compose)
- [Datos de demostración (Fixtures)](#datos-de-demostración-fixtures)
- [Endpoints de la API](#endpoints-de-la-api)
- [Tests del backend](#tests-del-backend)
- [Tests del frontend](#tests-del-frontend)
- [Licencia](#licencia)

---

## Descripción

API REST completa para gestionar peces, acuarios, iluminación, plantas y tareas de mantenimiento. Incluye autenticación JWT con roles (`ROLE_ADMIN` / `ROLE_USER`), un frontend SPA en Vue 3 y una batería completa de tests unitarios y funcionales tanto en backend como en frontend.

---

## Arquitectura y stack

| Capa | Tecnología | Versión |
|---|---|---|
| Backend | Python + FastAPI | 3.12 / 0.115+ |
| ORM | SQLAlchemy (async) | 2.0+ |
| Validación | Pydantic | v2 |
| Base de datos | MySQL | 8.0 |
| Driver async | aiomysql | latest |
| Auth | python-jose + bcrypt | latest |
| Frontend | Vue 3 + Vite + Pinia | 3.x / 5.x / 2.x |
| Tests backend | pytest + pytest-asyncio + httpx | 9.x / 1.3+ / 0.23+ |
| Tests frontend | Vitest + @vue/test-utils | 1.x / 2.x |
| Orquestación | Docker Compose | v2 |

---

## Requisitos

- Docker y Docker Compose instalados
- (Opcional) Node.js ≥ 18 y npm para desarrollo frontend local

---

## Estructura de carpetas

```
ssd-pez-py/
├── Dockerfile
├── docker-compose.yml
├── Makefile                  ← Comandos de gestión del proyecto
├── openapi.yaml              ← Contrato SDD (fuente de verdad)
├── requirements.txt
├── pytest.ini
├── Readme.md
├── app/
│   ├── main.py               # Punto de entrada FastAPI
│   ├── auth.py               # Lógica JWT: hashing, tokens, dependencias
│   ├── database.py           # Conexión async SQLAlchemy
│   ├── models.py             # Modelos ORM (tablas MySQL, modelo User)
│   ├── schemas.py            # Modelos Pydantic v2 (contrato OpenAPI)
│   ├── crud.py               # Lógica de base de datos
│   ├── init_db.py            # Crea tablas y usuario admin por defecto
│   ├── fixtures.py           # Datos de demostración (2 acuarios, peces, plantas…)
│   ├── routers/
│   │   ├── auth.py           # POST /auth/login|register|refresh, GET /auth/me
│   │   ├── acuario.py
│   │   ├── fish.py
│   │   ├── plants.py
│   │   ├── lighting.py
│   │   └── maintenance.py
│   └── tests/
│       ├── __init__.py
│       ├── test_api.py       # Tests CRUD completos (23 tests, todas las entidades)
│       ├── test_auth.py      # Tests de autenticación JWT (login, /me)
│       └── test_acuario.py   # Tests CRUD de acuario con auth (crear, listar, eliminar)
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── vitest.config.js      ← Configuración de Vitest con alias @ y jsdom
    └── src/
        ├── App.vue
        ├── main.js
        ├── api/              # Clientes axios por entidad
        ├── components/
        │   ├── EntityForm.vue
        │   ├── EntityForm.test.js   # Tests del formulario genérico (5 tests)
        │   └── ...
        ├── composables/
        ├── router/
        ├── stores/
        │   ├── auth.js
        │   └── auth.test.js  # Tests del store de autenticación (4 tests)
        └── views/
```

---

## Pasos seguidos en SDD

### 1. Definir la especificación (`openapi.yaml`)
Crear el contrato completo de la API: endpoints, esquemas, parámetros de filtrado/paginación y seguridad Bearer JWT.

### 2. Preparar el entorno
- `Dockerfile` con imagen `python:3.12-slim`
- `requirements.txt` con todas las dependencias
- `docker-compose.yml` con tres servicios: `api`, `db` y `frontend`

### 3. Generar los schemas Pydantic v2 (`schemas.py`)
Siguiendo el spec, se definen los modelos de validación de entrada/salida para cada entidad: Fish, Plant, Acuario, Lighting, Maintenance.

> **Nota técnica:** Se usa la API moderna de Pydantic v2:
> `Field(min_length=..., ge=...)` en lugar de los deprecados `constr()`/`conint()`,
> y `model_config = ConfigDict(...)` en lugar de `class Config`.

### 4. Definir los modelos ORM (`models.py`)
Modelos SQLAlchemy 2.0 con `DeclarativeBase` (en lugar del deprecado `declarative_base()`), relaciones y claves foráneas entre entidades. Incluye el modelo `User` con roles (`ROLE_ADMIN`, `ROLE_USER`) para la autenticación.

### 5. Configurar la base de datos (`database.py`)
Motor async con `create_async_engine` y `AsyncSession`. Las tablas se crean automáticamente con `init_db.py`, que además siembra el usuario admin por defecto a partir de variables de entorno.

### 6. Implementar el CRUD (`crud.py` + `routers/`)
- Funciones async CRUD para cada entidad usando `select()` de SQLAlchemy 2.0
- Routers FastAPI por entidad con `Depends(get_db)` para inyección de sesión
- Se usa `.model_dump()` en lugar del deprecado `.dict()` de Pydantic v1

### 7. Tests del backend CRUD
Batería de 23 tests que cubre todas las operaciones CRUD de las cinco entidades.  
Ver sección [Tests del backend](#tests-del-backend).

### 8. Extender el spec con seguridad JWT (`openapi.yaml`)
Se añaden al contrato los endpoints de autenticación (`/auth/login`, `/auth/register`, `/auth/refresh`, `/auth/me`), el esquema `bearerAuth` y los roles de usuario. El spec sigue siendo la fuente de verdad.

### 9. Implementar autenticación JWT en el backend
- **`app/auth.py`**: hashing bcrypt, creación/verificación de tokens JWT (python-jose), dependencias `get_current_user` y `require_admin`
- **`app/routers/auth.py`**: endpoints de login, registro (solo admin), refresh y perfil
- Todos los endpoints CRUD quedan protegidos con `Depends(get_current_user)` o `Depends(require_admin)`

### 10. Desarrollar el frontend Vue 3 a partir del spec
SPA completa con Vue 3 + Vite + Pinia + Vue Router. A partir del spec y de un prompt de especificaciones (`ssd_front_prompt.md`) se genera:
- Store de autenticación con gestión automática de tokens y refresh interceptor en axios
- CRUD completo para cada entidad con componentes reutilizables (`EntityForm`, `EntityManager`)
- Guardas de ruta: páginas protegidas redirigen a `/login` si no hay sesión activa

### 11. Tests unitarios y funcionales completos
- **Backend**: 25 tests (pytest + httpx ASGITransport) cubriendo auth JWT y todos los endpoints CRUD
- **Frontend**: 9 tests (Vitest + @vue/test-utils) cubriendo el componente `EntityForm` y el store de autenticación  
Ver secciones [Tests del backend](#tests-del-backend) y [Tests del frontend](#tests-del-frontend).

### 12. Makefile para simplificar la operativa
Comandos `make start`, `make stop`, `make test`, `make ssh` y más para gestionar el proyecto sin tener que recordar los comandos de Docker Compose.  
Ver sección [Arranque rápido con Makefile](#arranque-rápido-con-makefile).

### 13. Fixtures con datos de demostración
Script `app/fixtures.py` que siembra la base de datos con dos acuarios reales (Asiático y Gambario), sus peces, plantas, iluminación y un calendario de mantenimiento quincenal. Operación idempotente: si los datos ya existen, no los duplica.  
Ver sección [Datos de demostración](#datos-de-demostración-fixtures).

---

## Estado del proyecto (Roadmap SDD)

| Fase | Descripción | Estado |
|---|---|---|
| ✅ Fase 0 | Definir spec CRUD (`openapi.yaml`) | Completado |
| ✅ Fase 1 | Backend CRUD (modelos, schemas, routers, crud) | Completado |
| ✅ Fase 2 | Tests CRUD (23 tests, sin warnings) | Completado |
| ✅ Fase 3 | Extender spec con Auth JWT (`openapi.yaml`) | Completado |
| ✅ Fase 4 | Implementar Auth backend (modelo User, JWT, roles) | Completado |
| ✅ Fase 5 | Frontend Vue 3 (desde spec completo) | Completado |
| ✅ Fase 6 | Tests completos: 25 backend + 9 frontend | Completado |
| ✅ Fase 7 | Makefile con comandos de gestión del proyecto | Completado |
| ✅ Fase 8 | Fixtures con datos de demostración reales | Completado |

---

## Arranque rápido con Makefile

La forma más sencilla de gestionar el proyecto:

```sh
make start      # Inicia todos los servicios (api + db + frontend)
make stop       # Para todos los servicios
make test       # Ejecuta TODOS los tests (backend + frontend)
make ssh        # Abre una shell en el contenedor API
make fixtures   # Carga los datos de demostración
```

Todos los comandos disponibles:

```sh
make help
```

```
  Acuarium — Comandos disponibles
  ────────────────────────────────────────────────
  make start          Inicia todos los servicios
  make stop           Para todos los servicios
  make restart        Reinicia todos los servicios
  make build          Reconstruye las imágenes Docker
  make logs           Muestra logs en tiempo real
  ────────────────────────────────────────────────
  make test           Ejecuta TODOS los tests
  make test-backend   Ejecuta solo los tests del backend
  make test-frontend  Ejecuta solo los tests del frontend
  ────────────────────────────────────────────────
  make ssh            Abre shell en el contenedor API
  make ssh-db         Abre shell en el contenedor DB
  make ssh-frontend   Abre shell en el contenedor Frontend
  ────────────────────────────────────────────────
  make init-db        Inicializa la BD y crea el admin
  make fixtures       Carga datos de demostración
```

---

## Arranque manual con Docker Compose

### Primera vez

```sh
# 1. Construir imágenes
docker compose build

# 2. Arrancar servicios (api + db + frontend)
docker compose up -d

# 3. Crear tablas en MySQL y usuario admin por defecto
docker compose exec api bash -c "cd /app && python3 -m app.init_db"
# → "✓ Tablas creadas / verificadas correctamente."
# → "✓ Usuario admin creado."
```

### Acceso a los servicios

| Servicio | URL |
|---|---|
| API REST (FastAPI) | http://localhost:8000 |
| Swagger UI (docs interactivos) | http://localhost:8000/docs |
| Frontend Vite/Vue 3 | http://localhost:5173 |
| MySQL | localhost:3306 |

### Parar servicios

```sh
docker compose down
```

---

## Datos de demostración (Fixtures)

El script `app/fixtures.py` siembra la base de datos con datos reales de acuariofilia para poder explorar la aplicación sin tener que introducir datos a mano.

### Qué se carga

| Entidad | Datos |
|---|---|
| **Acuarios** | Asiático (600 L) · Gambario (30 L) |
| **Peces** | Gurami Perla · Gurami Samurai · Garra Flavatra *(Asiático)* — Neocaridina Azul *(Gambario)* |
| **Plantas** | Anubias Barteri · Echinodorus Ozelot · Sagitaria Subulata *(Asiático)* |
| **Iluminación** | LED Full Spectrum 30 W WiFi *(Asiático)* · LED Planted 10 W *(Gambario)* |
| **Mantenimiento** | 4 tareas quincenal en Asiático + 4 en Gambario (cambios de agua y limpieza de filtros) |

> ⚠️ El script es **idempotente**: si el acuario "Asiático" ya existe en la BD, no se duplica ningún registro.

### Cargar los fixtures

```sh
# Con Makefile (recomendado):
make fixtures

# O directamente con Docker Compose:
docker compose exec api bash -c "cd /app && python3 -m app.fixtures"
```

**Resultado esperado:**
```
⏳ Cargando fixtures de demostración…

  ✓ Acuario 'Asiático'  creado  (id=1,  600 L)
  ✓ Acuario 'Gambario'  creado  (id=2,   30 L)
  ✓ 4 peces cargados  (3 en Asiático: Gurami Perla, Gurami Samurai, Garra Flavatra · 1 en Gambario: Neocaridina Azul)
  ✓ 3 plantas cargadas  (Anubias Barteri, Echinodorus Ozelot, Sagitaria Subulata)
  ✓ 2 focos de iluminación cargados  (LED 30 W en Asiático · LED 10 W en Gambario)
  ✓ 8 tareas de mantenimiento quincenal cargadas

✅ ¡Fixtures cargados con éxito!
   Visita http://localhost:5173 para explorar los datos de demostración.
```

Si se ejecuta de nuevo cuando los datos ya existen:
```
✓ Los fixtures de demostración ya están cargados — nada que hacer.
```

### Flujo completo desde cero

```sh
make start      # 1. Levanta los contenedores
make init-db    # 2. Crea las tablas y el usuario admin
make fixtures   # 3. Carga los datos de demostración
```

Después, abre **http://localhost:5173** e inicia sesión con `admin / Admin1234!`.

---

## Endpoints de la API

Todos los endpoints aceptan y devuelven **JSON**. Los endpoints CRUD requieren autenticación Bearer JWT. Los de eliminación requieren `ROLE_ADMIN`.

### Auth

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `POST` | `/auth/login` | ❌ Público | Obtener access + refresh token |
| `POST` | `/auth/register` | ✅ Admin | Registrar nuevo usuario |
| `POST` | `/auth/refresh` | ❌ Público | Renovar access token |
| `GET` | `/auth/me` | ✅ Usuario | Perfil del usuario autenticado |

### Acuario
Soporta paginación con `?skip=0&limit=20`.

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/acuario/` | ✅ Usuario | Listar acuarios |
| `GET` | `/acuario/{id}` | ✅ Usuario | Obtener acuario por ID |
| `POST` | `/acuario/` | ✅ Usuario | Crear acuario |
| `PUT` | `/acuario/{id}` | ✅ Usuario | Actualizar acuario |
| `DELETE` | `/acuario/{id}` | ✅ Admin | Eliminar acuario |

### Fish

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/fish/` | ✅ Usuario | Listar peces |
| `GET` | `/fish/{id}` | ✅ Usuario | Obtener pez por ID |
| `POST` | `/fish/` | ✅ Usuario | Crear pez |
| `PUT` | `/fish/{id}` | ✅ Usuario | Actualizar pez |
| `DELETE` | `/fish/{id}` | ✅ Admin | Eliminar pez |

### Plants

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/plants/` | ✅ Usuario | Listar plantas |
| `GET` | `/plants/{id}` | ✅ Usuario | Obtener planta por ID |
| `POST` | `/plants/` | ✅ Usuario | Crear planta |
| `PUT` | `/plants/{id}` | ✅ Usuario | Actualizar planta |
| `DELETE` | `/plants/{id}` | ✅ Admin | Eliminar planta |

### Lighting

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/lighting/` | ✅ Usuario | Listar iluminaciones |
| `GET` | `/lighting/{id}` | ✅ Usuario | Obtener por ID |
| `POST` | `/lighting/` | ✅ Usuario | Crear iluminación |
| `PUT` | `/lighting/{id}` | ✅ Usuario | Actualizar |
| `DELETE` | `/lighting/{id}` | ✅ Admin | Eliminar |

### Maintenance

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| `GET` | `/maintenance/` | ✅ Usuario | Listar tareas |
| `GET` | `/maintenance/{id}` | ✅ Usuario | Obtener por ID |
| `POST` | `/maintenance/` | ✅ Usuario | Crear tarea |
| `PUT` | `/maintenance/{id}` | ✅ Usuario | Actualizar |
| `DELETE` | `/maintenance/{id}` | ✅ Admin | Eliminar |

### Ejemplo rápido con autenticación

```bash
# 1. Obtener token
TOKEN=$(curl -s -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "Admin1234!"}' \
     | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 2. Usar el token para crear un pez
curl -X POST "http://localhost:8000/fish/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
           "name": "Nemo",
           "species": "Amphiprioninae",
           "age": 2,
           "behavior": "Pacífico",
           "area_of_tank": "Zona media",
           "picture": "https://example.com/nemo.jpg",
           "acuarioId": 1
         }'
```

Explora todos los endpoints con el Swagger interactivo: **http://localhost:8000/docs**

---

## Tests del backend

### Descripción

La batería de pruebas verifica los endpoints de autenticación y todos los endpoints CRUD de la API. Se ejecutan **directamente contra la base de datos MySQL** sin levantar un servidor HTTP adicional, gracias a `httpx.ASGITransport`.

**Cobertura: 25 tests · auth + 5 entidades · 0 warnings**

| Archivo | Tests | Cobertura |
|---|---|---|
| `test_api.py` | 23 | CRUD completo: Acuario, Fish, Plants, Lighting, Maintenance |
| `test_auth.py` | 1 | Login y perfil `/auth/me` con token JWT |
| `test_acuario.py` | 1 | Ciclo completo crear → listar → eliminar con auth |

### Decisiones técnicas

- **`httpx.ASGITransport`**: conecta directamente con la app ASGI sin servidor HTTP. *(El parámetro `app=` fue eliminado en httpx 0.20+)*
- **`pytest-asyncio` modo `auto`**: todos los tests y fixtures async se marcan automáticamente.
- **Event loop `session`-scoped**: un único event loop para toda la sesión de tests, evitando el error *"Future attached to a different loop"* que ocurre con conexiones async de SQLAlchemy entre tests.
- **Fixture `client` autenticada**: la fixture base hace login como admin y añade el Bearer token a todas las peticiones, ya que todos los endpoints requieren autenticación.
- **`pythonpath = .`** en `pytest.ini`: permite que `from app.main import app` resuelva correctamente desde el directorio raíz del proyecto.

### Configuración (`pytest.ini`)

```ini
[pytest]
asyncio_mode = auto
asyncio_default_fixture_loop_scope = session
asyncio_default_test_loop_scope = session
pythonpath = .
```

### Ejecutar los tests

```sh
# Con Makefile (recomendado):
make test-backend

# O directamente con Docker Compose:
docker compose exec api bash -c "cd /app && pytest app/tests/ -v"
```

**Resultado esperado:**
```
collected 25 items

app/tests/test_acuario.py::test_acuario_crud          PASSED  [  4%]
app/tests/test_api.py::test_create_acuario             PASSED  [  8%]
...
app/tests/test_api.py::test_get_maintenance_not_found  PASSED  [ 96%]
app/tests/test_auth.py::test_login_and_me              PASSED  [100%]

============================== 25 passed in 7.25s ==============================
```

---

## Tests del frontend

### Descripción

Los tests del frontend verifican el componente genérico de formulario y el store de autenticación usando Vitest y `@vue/test-utils`, con entorno `jsdom` para simular el DOM del navegador.

**Cobertura: 9 tests · 2 archivos · 0 warnings**

| Archivo | Tests | Cobertura |
|---|---|---|
| `EntityForm.test.js` | 5 | Renderizado, submit con datos válidos, validación de errores, carga de datos iniciales, botón cancelar |
| `auth.test.js` | 4 | Estado inicial, login/logout, rol admin, limpieza de localStorage |

### Decisiones técnicas

- **Vitest** en lugar de Jest: integración nativa con Vite, sin configuración adicional de transformadores.
- **`@vue/test-utils`**: montaje de componentes Vue 3 con soporte completo de Composition API y `<script setup>`.
- **`vi.mock()`**: los tests del store mockean `@/api/auth` y `@/router` para aislar la lógica del store de las llamadas HTTP reales.
- **`jsdom`**: entorno DOM que emula `localStorage`, eventos del navegador y renderizado de componentes sin necesidad de un navegador real.
- **`vitest.config.js`** separado de `vite.config.js`: necesario para que el alias `@` se resuelva correctamente en el entorno de test.

### Configuración (`vitest.config.js`)

```js
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) }
  },
  test: {
    environment: 'jsdom',
    globals: true,
  }
})
```

### Ejecutar los tests

```sh
# Con Makefile (recomendado):
make test-frontend

# O directamente con Docker Compose:
docker compose exec frontend sh -c "cd /app && npm run test"
```

**Resultado esperado:**
```
 ✓ src/stores/auth.test.js        (4 tests)
 ✓ src/components/EntityForm.test.js  (5 tests)

 Test Files  2 passed (2)
      Tests  9 passed (9)
```

---

## Licencia

MIT
