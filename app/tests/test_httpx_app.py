"""Script auxiliar para probar la conexión básica con httpx + ASGITransport."""
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
import asyncio

app = FastAPI()


async def main():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.get("/")
        print(resp.status_code)


if __name__ == "__main__":
    asyncio.run(main())
