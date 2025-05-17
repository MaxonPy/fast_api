from aiohttp import web
from app.auth import create_access_token, token_required
from .models import Book
from app.db import add_book_to_db, delete_book_from_db, get_books_from_db

async def login(request):
    """логин пользователя
    проверяю креды и отдаю токен если всё ок
    """
    data = await request.json()
    if data.get("username") == "user" and data.get("password") == "password":
        token = create_access_token({"username": data["username"]})
        return web.json_response({"access_token": token})
    return web.HTTPUnauthorized(text="Invalid credentials")

@token_required
async def add_book(request):
    """добавляю новую книгу в БД
    нужен токен для доступа
    """
    data = await request.json()
    book = Book(**data)
    db = request.app["db"]
    result = await add_book_to_db(db, book)
    return web.json_response(result)

@token_required
async def delete_book(request):
    """удаляю книгу по ID
    если не нашел - верну 404
    """
    book_id = int(request.match_info["book_id"])
    db = request.app["db"]
    result = await delete_book_from_db(db, book_id)
    if result["status"] == "success":
        return web.json_response({"status": "книга удалена"})
    else:
        raise web.HTTPNotFound(text="книга не найдена")


@token_required
async def get_books(request):
    """получаю список книг
    пагинация через offset и limit
    """
    db = request.app["db"]
    offset = int(request.query.get("offset", 0))
    limit = int(request.query.get("limit", 10))
    books = await get_books_from_db(db, offset, limit)
    return web.json_response({"books": books})


def setup_routes(app):
    """настройка маршрутов для api"""
    app.router.add_post("/login", login)  
    app.router.add_post("/books", add_book)  
    app.router.add_delete("/books/{book_id}", delete_book)  
    app.router.add_get("/books", get_books)  
