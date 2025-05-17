import pytest
from aiohttp import web
from app.auth import create_access_token, token_required
from app.routes import login, add_book

@pytest.fixture
async def client(aiohttp_client):
    """фикстура для создания тестового клиента
        добавляет защищенный маршрут, который требует токен для доступа"""
    app = web.Application()
    app.router.add_post("/login", login)
    app.router.add_post("/books", add_book)

    # защищенный токеном
    @token_required
    async def protected_handler(request):
        return web.json_response({"message": "все ок"})
    app.router.add_get("/protected", protected_handler)
    return await aiohttp_client(app)

@pytest.fixture
def mock_access_token():
    return create_access_token({
        "username": "user",
        "password": "password"
    })
