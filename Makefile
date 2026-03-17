# ============================================================
#  Makefile — Acuarium Management API
#  Uso: make <comando>
# ============================================================

DC        = docker compose
API       = $(DC) exec api
FRONTEND  = $(DC) exec frontend sh -c

.PHONY: help start stop restart build logs \
        test test-backend test-frontend \
        ssh ssh-db ssh-frontend \
        shell-db init-db fixtures

# ── Ayuda ────────────────────────────────────────────────────
help:
	@echo ""
	@echo "  Acuarium — Comandos disponibles"
	@echo "  ────────────────────────────────────────────────"
	@echo "  make start          Inicia todos los servicios"
	@echo "  make stop           Para todos los servicios"
	@echo "  make restart        Reinicia todos los servicios"
	@echo "  make build          Reconstruye las imágenes Docker"
	@echo "  make logs           Muestra logs en tiempo real"
	@echo "  ────────────────────────────────────────────────"
	@echo "  make test           Ejecuta TODOS los tests"
	@echo "  make test-backend   Ejecuta solo los tests del backend"
	@echo "  make test-frontend  Ejecuta solo los tests del frontend"
	@echo "  ────────────────────────────────────────────────"
	@echo "  make ssh            Abre shell en el contenedor API"
	@echo "  make ssh-db         Abre shell en el contenedor DB"
	@echo "  make ssh-frontend   Abre shell en el contenedor Frontend"
	@echo "  ────────────────────────────────────────────────"
	@echo "  make init-db        Inicializa la BD y crea el admin"
	@echo "  make fixtures       Carga datos de demostración"
	@echo ""

# ── Ciclo de vida ────────────────────────────────────────────
start:
	@echo "🚀 Iniciando todos los servicios..."
	$(DC) up -d
	@echo ""
	@echo "  ✅ Servicios en marcha:"
	@echo "     · API      →  http://localhost:8000"
	@echo "     · Docs     →  http://localhost:8000/docs"
	@echo "     · Frontend →  http://localhost:5173"
	@echo ""

stop:
	@echo "🛑 Parando todos los servicios..."
	$(DC) down

restart:
	@echo "🔄 Reiniciando todos los servicios..."
	$(DC) restart

build:
	@echo "🔨 Reconstruyendo imágenes Docker..."
	$(DC) build --no-cache

logs:
	$(DC) logs -f

# ── Tests ────────────────────────────────────────────────────
test: test-backend test-frontend

test-backend:
	@echo "🐍 Ejecutando tests del backend (pytest)..."
	$(API) bash -c "cd /app && pytest app/tests/ -v"

test-frontend:
	@echo "🟣 Ejecutando tests del frontend (vitest)..."
	$(FRONTEND) "cd /app && npm run test"

# ── SSH / Consolas ───────────────────────────────────────────
ssh:
	@echo "🔗 Conectando al contenedor API..."
	$(API) bash

ssh-db:
	@echo "🔗 Conectando al contenedor DB (MySQL)..."
	$(DC) exec db bash

ssh-frontend:
	@echo "🔗 Conectando al contenedor Frontend..."
	$(DC) exec frontend sh

# ── Base de datos ────────────────────────────────────────────
init-db:
	@echo "🗄️  Inicializando base de datos y creando usuario admin..."
	$(API) bash -c "cd /app && python3 -m app.init_db"

fixtures:
	@echo "🐠 Cargando datos de demostración (fixtures)..."
	$(API) bash -c "cd /app && python3 -m app.fixtures"

