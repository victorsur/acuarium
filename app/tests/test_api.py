"""
Batería de pruebas de integración para la API de Acuario.

Se utiliza httpx.ASGITransport para conectar directamente con la app FastAPI
sin necesidad de levantar un servidor HTTP real. Los tests se ejecutan contra
la base de datos MySQL configurada en DATABASE_URL.

Ejecución (dentro del contenedor):
    docker compose run --rm -w /app api pytest app/tests/ -v
"""

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# ---------------------------------------------------------------------------
# Fixture: cliente HTTP reutilizable para todos los tests
# ---------------------------------------------------------------------------

@pytest.fixture
async def client():
    """AsyncClient configurado para comunicarse directamente con la app ASGI.
    Se autentica automáticamente como admin antes de ceder el control a los tests."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        resp = await ac.post("/auth/login", json={"username": "admin", "password": "Admin1234!"})
        token = resp.json()["access_token"]
        ac.headers.update({"Authorization": f"Bearer {token}"})
        yield ac


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def create_acuario(client: AsyncClient, name: str = "Acuario Test") -> int:
    resp = await client.post("/acuario/", json={"name": name, "volume": 200})
    assert resp.status_code == 201, f"Error creando acuario: {resp.text}"
    return resp.json()["id"]


async def delete_acuario(client: AsyncClient, acuario_id: int):
    await client.delete(f"/acuario/{acuario_id}")


# ===========================================================================
# TESTS: Acuario
# ===========================================================================

async def test_create_acuario(client):
    resp = await client.post("/acuario/", json={"name": "Mi Acuario", "volume": 150})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Mi Acuario"
    assert data["volume"] == 150
    await client.delete(f"/acuario/{data['id']}")


async def test_list_acuarios(client):
    acuario_id = await create_acuario(client, "Acuario Lista")
    resp = await client.get("/acuario/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
    assert acuario_id in [a["id"] for a in resp.json()]
    await delete_acuario(client, acuario_id)


async def test_get_acuario(client):
    acuario_id = await create_acuario(client, "Acuario Get")
    resp = await client.get(f"/acuario/{acuario_id}")
    assert resp.status_code == 200
    assert resp.json()["id"] == acuario_id
    await delete_acuario(client, acuario_id)


async def test_update_acuario(client):
    acuario_id = await create_acuario(client, "Acuario Original")
    resp = await client.put(f"/acuario/{acuario_id}", json={"name": "Acuario Actualizado", "volume": 300})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Acuario Actualizado"
    await delete_acuario(client, acuario_id)


async def test_delete_acuario(client):
    acuario_id = await create_acuario(client, "Acuario Delete")
    resp = await client.delete(f"/acuario/{acuario_id}")
    assert resp.status_code == 204
    assert (await client.get(f"/acuario/{acuario_id}")).status_code == 404


async def test_get_acuario_not_found(client):
    resp = await client.get("/acuario/999999")
    assert resp.status_code == 404


# ===========================================================================
# TESTS: Fish
# ===========================================================================

@pytest.fixture
async def acuario_id(client):
    aid = await create_acuario(client, "Acuario para Fish")
    yield aid
    await delete_acuario(client, aid)


FISH_DATA = {
    "name": "Nemo",
    "species": "Amphiprioninae",
    "age": 2,
    "behavior": "Pacífico",
    "area_of_tank": "Zona media",
    "picture": "https://example.com/nemo.jpg",
}


async def test_create_fish(client, acuario_id):
    resp = await client.post("/fish/", json={**FISH_DATA, "acuarioId": acuario_id})
    assert resp.status_code == 201
    fish = resp.json()
    assert fish["name"] == "Nemo"
    await client.delete(f"/fish/{fish['id']}")


async def test_list_fish(client, acuario_id):
    fish_id = (await client.post("/fish/", json={**FISH_DATA, "acuarioId": acuario_id})).json()["id"]
    resp = await client.get("/fish/")
    assert resp.status_code == 200
    assert any(f["id"] == fish_id for f in resp.json())
    await client.delete(f"/fish/{fish_id}")


async def test_get_fish(client, acuario_id):
    fish_id = (await client.post("/fish/", json={**FISH_DATA, "acuarioId": acuario_id})).json()["id"]
    resp = await client.get(f"/fish/{fish_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Nemo"
    await client.delete(f"/fish/{fish_id}")


async def test_update_fish(client, acuario_id):
    fish_id = (await client.post("/fish/", json={**FISH_DATA, "acuarioId": acuario_id})).json()["id"]
    update = {**FISH_DATA, "name": "Nemo Actualizado", "age": 5, "acuarioId": acuario_id}
    resp = await client.put(f"/fish/{fish_id}", json=update)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Nemo Actualizado"
    await client.delete(f"/fish/{fish_id}")


async def test_delete_fish(client, acuario_id):
    fish_id = (await client.post("/fish/", json={**FISH_DATA, "acuarioId": acuario_id})).json()["id"]
    resp = await client.delete(f"/fish/{fish_id}")
    assert resp.status_code == 204
    assert (await client.get(f"/fish/{fish_id}")).status_code == 404


async def test_get_fish_not_found(client):
    assert (await client.get("/fish/999999")).status_code == 404


# ===========================================================================
# TESTS: Plants
# ===========================================================================

@pytest.fixture
async def acuario_id_plants(client):
    aid = await create_acuario(client, "Acuario para Plants")
    yield aid
    await delete_acuario(client, aid)


PLANT_DATA = {
    "name": "Anubias",
    "species": "Anubias barteri",
    "age": 1,
    "picture": "https://example.com/anubias.jpg",
    "description": "Planta resistente y de bajo mantenimiento.",
}


async def test_create_plant(client, acuario_id_plants):
    resp = await client.post("/plants/", json={**PLANT_DATA, "acuarioId": acuario_id_plants})
    assert resp.status_code == 201
    plant = resp.json()
    assert plant["name"] == "Anubias"
    await client.delete(f"/plants/{plant['id']}")


async def test_list_plants(client, acuario_id_plants):
    plant_id = (await client.post("/plants/", json={**PLANT_DATA, "acuarioId": acuario_id_plants})).json()["id"]
    resp = await client.get("/plants/")
    assert resp.status_code == 200
    assert any(p["id"] == plant_id for p in resp.json())
    await client.delete(f"/plants/{plant_id}")


async def test_get_plant(client, acuario_id_plants):
    plant_id = (await client.post("/plants/", json={**PLANT_DATA, "acuarioId": acuario_id_plants})).json()["id"]
    resp = await client.get(f"/plants/{plant_id}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Anubias"
    await client.delete(f"/plants/{plant_id}")


async def test_delete_plant(client, acuario_id_plants):
    plant_id = (await client.post("/plants/", json={**PLANT_DATA, "acuarioId": acuario_id_plants})).json()["id"]
    resp = await client.delete(f"/plants/{plant_id}")
    assert resp.status_code == 204
    assert (await client.get(f"/plants/{plant_id}")).status_code == 404


async def test_get_plant_not_found(client):
    assert (await client.get("/plants/999999")).status_code == 404


# ===========================================================================
# TESTS: Lighting
# ===========================================================================

@pytest.fixture
async def acuario_id_lighting(client):
    aid = await create_acuario(client, "Acuario para Lighting")
    yield aid
    await delete_acuario(client, aid)


LIGHTING_DATA = {
    "light_type": "LED",
    "watts": 20,
    "wifi": True,
    "start_time": "08:00",
    "end_time": "20:00",
}


async def test_create_lighting(client, acuario_id_lighting):
    data = {**LIGHTING_DATA, "aquariumId": acuario_id_lighting}
    resp = await client.post("/lighting/", json=data)
    assert resp.status_code == 201
    light = resp.json()
    assert light["light_type"] == "LED"
    await client.delete(f"/lighting/{light['id']}")


async def test_list_lighting(client, acuario_id_lighting):
    light_id = (await client.post("/lighting/", json={**LIGHTING_DATA, "aquariumId": acuario_id_lighting})).json()["id"]
    resp = await client.get("/lighting/")
    assert resp.status_code == 200
    assert any(l["id"] == light_id for l in resp.json())
    await client.delete(f"/lighting/{light_id}")


async def test_get_lighting_not_found(client):
    assert (await client.get("/lighting/999999")).status_code == 404


# ===========================================================================
# TESTS: Maintenance
# ===========================================================================

@pytest.fixture
async def acuario_id_maintenance(client):
    aid = await create_acuario(client, "Acuario para Maintenance")
    yield aid
    await delete_acuario(client, aid)


MAINTENANCE_DATA = {
    "task": "Cambio de agua parcial 30%",
    "date": "2026-03-16T10:00:00",
}


async def test_create_maintenance(client, acuario_id_maintenance):
    data = {**MAINTENANCE_DATA, "acuarioId": acuario_id_maintenance}
    resp = await client.post("/maintenance/", json=data)
    assert resp.status_code == 201
    m = resp.json()
    assert m["task"] == "Cambio de agua parcial 30%"
    await client.delete(f"/maintenance/{m['id']}")


async def test_list_maintenance(client, acuario_id_maintenance):
    m_id = (await client.post("/maintenance/", json={**MAINTENANCE_DATA, "acuarioId": acuario_id_maintenance})).json()["id"]
    resp = await client.get("/maintenance/")
    assert resp.status_code == 200
    assert any(m["id"] == m_id for m in resp.json())
    await client.delete(f"/maintenance/{m_id}")


async def test_get_maintenance_not_found(client):
    assert (await client.get("/maintenance/999999")).status_code == 404
