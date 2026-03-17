import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_acuario_crud():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Login
        resp = await ac.post("/auth/login", json={"username": "admin", "password": "Admin1234!"})
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Crear acuario
        resp = await ac.post("/acuario/", json={"name": "TestAcuario", "volume": 123}, headers=headers)
        assert resp.status_code == 201
        acuario = resp.json()
        assert acuario["name"] == "TestAcuario"

        # Listar acuarios
        resp = await ac.get("/acuario/", headers=headers)
        assert resp.status_code == 200
        assert any(a["name"] == "TestAcuario" for a in resp.json())

        # Eliminar acuario (requiere admin, que ya tenemos)
        resp = await ac.delete(f"/acuario/{acuario['id']}", headers=headers)
        assert resp.status_code == 204
