import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_login_and_me():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Login
        resp = await ac.post("/auth/login", json={"username": "admin", "password": "Admin1234!"})
        assert resp.status_code == 200
        tokens = resp.json()
        assert "access_token" in tokens

        # Me
        headers = {"Authorization": f"Bearer {tokens['access_token']}"}
        resp = await ac.get("/auth/me", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["username"] == "admin"

