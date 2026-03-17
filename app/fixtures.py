"""
app/fixtures.py — Datos de demostración para el acuario.

Carga dos acuarios de ejemplo con sus peces, plantas, iluminación y
tareas de mantenimiento quincenal. La operación es idempotente: si el
acuario 'Asiático' ya existe en la BD, no se duplica ningún dato.

Uso:
    python -m app.fixtures
"""
import asyncio
from datetime import datetime

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Acuario, Fish, Plant, Lighting, Maintenance


# ─── Fechas de mantenimiento (quincenales) ─────────────────────────────────

Q1 = datetime(2026, 4,  1, 10, 0, 0)   # 1ª quincena de abril
Q2 = datetime(2026, 4, 15, 10, 0, 0)   # 2ª quincena de abril
Q3 = datetime(2026, 5,  1, 10, 0, 0)   # 1ª quincena de mayo
Q4 = datetime(2026, 5, 15, 10, 0, 0)   # 2ª quincena de mayo


# ─── Constructores de datos ─────────────────────────────────────────────────

def _fish(asiatico_id: int, gambario_id: int) -> list[dict]:
    return [
        # ── Acuario Asiático ─────────────────────────────────────────────
        {
            "name":         "Gurami Perla",
            "species":      "Trichogaster leeri",
            "age":          2,
            "behavior":     "Pacífico, ligeramente territorial entre machos",
            "area_of_tank": "Zona media",
            "picture":      "https://upload.wikimedia.org/wikipedia/commons/e/e0/Trichogaster_leeri.jpg",
            "acuarioId":    asiatico_id,
        },
        {
            "name":         "Gurami Samurai",
            "species":      "Sphaerichthys vaillanti", # Corregido: El Samurai es S. vaillanti
            "age":          1,
            "behavior":     "Semipacífico, suave con otras especies",
            "area_of_tank": "Zona media y alta",
            "picture":      "https://upload.wikimedia.org/wikipedia/commons/d/d4/Sphaerichthys_vaillanti_male.jpg",
            "acuarioId":    asiatico_id,
        },
        {
            "name":         "Garra Flavatra",
            "species":      "Garra flavatra",
            "age":          3,
            "behavior":     "Activo y sociable, raedor de algas",
            "area_of_tank": "Fondo y zona media",
            "picture":      "https://upload.wikimedia.org/wikipedia/commons/7/7b/Garra_flavatra_01.jpg",
            "acuarioId":    asiatico_id,
        },
        # ── Gambario ─────────────────────────────────────────────────────
        {
            "name":         "Neocaridina Azul",
            "species":      "Neocaridina davidi var. blue",
            "age":          1,
            "behavior":     "Pacífico, limpiador de algas y restos",
            "area_of_tank": "Fondo y musgo",
            "picture":      "https://upload.wikimedia.org/wikipedia/commons/0/03/Neocaridina_davidi_Blue_Dream.jpg",
            "acuarioId":    gambario_id,
        },
    ]


def _plants(asiatico_id: int) -> list[dict]:
    return [
        {
            "name":        "Anubias Barteri",
            "species":     "Anubias barteri",
            "age":         2,
            "picture":     "https://upload.wikimedia.org/wikipedia/commons/0/0c/Anubias_barteri_var._nana_01.jpg",
            "acuarioId":   asiatico_id,
            "description": "Resistente y de bajo mantenimiento. Ideal atada a rocas o madera.",
        },
        {
            "name":        "Echinodorus Ozelot",
            "species":     "Echinodorus ozelot",
            "age":         1,
            "picture":     "https://img.fruugo.com/product/3/89/1018698893_max.jpg",
            "acuarioId":   asiatico_id,
            "description": "Espada de mediano porte con hojas manchadas. Requiere sustrato nutritivo.",
        },
        {
            "name":        "Sagitaria Subulata",
            "species":     "Sagittaria subulata",
            "age":         1,
            "picture":     "https://pothos-vivas.com/wp-content/uploads/2021/01/sagittaria-subulata.jpg",
            "acuarioId":   asiatico_id,
            "description": "Tapizante de rápido crecimiento. Perfecta para fondos y bordes del acuario.",
        },
    ]


def _lighting(asiatico_id: int, gambario_id: int) -> list[dict]:
    return [
        {
            "light_type": "LED Full Spectrum",
            "watts":      30,
            "wifi":       True,
            "start_time": "10:00",
            "end_time":   "22:00",
            "aquariumId": asiatico_id,
        },
        {
            "light_type": "LED Planted",
            "watts":      10,
            "wifi":       False,
            "start_time": "10:00",
            "end_time":   "20:00",
            "aquariumId": gambario_id,
        },
    ]


def _maintenance(asiatico_id: int, gambario_id: int) -> list[dict]:
    return [
        # ── Asiático ─────────────────────────────────────────────────────
        {"task": "Cambio parcial de agua 30% — Asiático",      "date": Q1, "acuarioId": asiatico_id},
        {"task": "Limpieza de filtros — Asiático",              "date": Q2, "acuarioId": asiatico_id},
        {"task": "Cambio parcial de agua 30% — Asiático",      "date": Q3, "acuarioId": asiatico_id},
        {"task": "Limpieza de filtros — Asiático",              "date": Q4, "acuarioId": asiatico_id},
        # ── Gambario ─────────────────────────────────────────────────────
        {"task": "Cambio parcial de agua 20% — Gambario",      "date": Q1, "acuarioId": gambario_id},
        {"task": "Limpieza de filtro de esponja — Gambario",   "date": Q2, "acuarioId": gambario_id},
        {"task": "Cambio parcial de agua 20% — Gambario",      "date": Q3, "acuarioId": gambario_id},
        {"task": "Limpieza de filtro de esponja — Gambario",   "date": Q4, "acuarioId": gambario_id},
    ]


# ─── Script principal ───────────────────────────────────────────────────────

async def load_fixtures() -> None:
    async with AsyncSessionLocal() as db:

        # Idempotencia: si 'Asiático' ya existe no duplicamos nada
        existing = (await db.execute(
            select(Acuario).where(Acuario.name == "Asiático")
        )).scalar_one_or_none()

        if existing:
            print("✓ Los fixtures de demostración ya están cargados — nada que hacer.")
            return

        print("⏳ Cargando fixtures de demostración…\n")

        # ── Acuarios ──────────────────────────────────────────────────────
        asiatico = Acuario(name="Asiático", volume=600)
        gambario  = Acuario(name="Gambario",  volume=30)
        db.add(asiatico)
        db.add(gambario)
        await db.flush()          # obtiene los IDs sin hacer commit aún
        print(f"  ✓ Acuario 'Asiático'  creado  (id={asiatico.id},  600 L)")
        print(f"  ✓ Acuario 'Gambario'  creado  (id={gambario.id},   30 L)")

        # ── Peces ──────────────────────────────────────────────────────────
        fish_rows = _fish(asiatico.id, gambario.id)
        for row in fish_rows:
            db.add(Fish(**row))
        await db.flush()
        print(f"  ✓ {len(fish_rows)} peces cargados"
              f"  (3 en Asiático: Gurami Perla, Gurami Samurai, Garra Flavatra"
              f" · 1 en Gambario: Neocaridina Azul)")

        # ── Plantas ────────────────────────────────────────────────────────
        plant_rows = _plants(asiatico.id)
        for row in plant_rows:
            db.add(Plant(**row))
        await db.flush()
        print(f"  ✓ {len(plant_rows)} plantas cargadas"
              f"  (Anubias Barteri, Echinodorus Ozelot, Sagitaria Subulata)")

        # ── Iluminación ────────────────────────────────────────────────────
        light_rows = _lighting(asiatico.id, gambario.id)
        for row in light_rows:
            db.add(Lighting(**row))
        await db.flush()
        print(f"  ✓ {len(light_rows)} focos de iluminación cargados"
              f"  (LED 30 W en Asiático · LED 10 W en Gambario)")

        # ── Mantenimiento ──────────────────────────────────────────────────
        maint_rows = _maintenance(asiatico.id, gambario.id)
        for row in maint_rows:
            db.add(Maintenance(**row))
        await db.flush()
        print(f"  ✓ {len(maint_rows)} tareas de mantenimiento quincenal cargadas")

        await db.commit()
        print("\n✅ ¡Fixtures cargados con éxito!")
        print("   Visita http://localhost:5173 para explorar los datos de demostración.")


if __name__ == "__main__":
    asyncio.run(load_fixtures())

