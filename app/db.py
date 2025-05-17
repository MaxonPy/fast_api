import asyncpg
from app.config import DATABASE_URL
from app.models import Book


async def init_db():
    """Создаю пул подключений к БД."""
    return await asyncpg.create_pool(DATABASE_URL) 


async def add_book_to_db(pool, book: Book):
    """Добавляю книгу в БД
    
    Возвращаю инфу о добавленной книге
    """

    async with pool.acquire() as conn:  # соединение из пула
        result = await conn.fetchrow(
            "INSERT INTO books (title, author, year, isbn) VALUES ($1, $2, $3, $4) RETURNING *",
            book.title, book.author, book.year, book.isbn
        )
        return dict(result)  


async def delete_book_from_db(pool, book_id: int):
    """Удаляю книгу по ID
    
    Возвращаю статус: success если удалил, not_found если нет такой книги
    """

    async with pool.acquire() as conn:
        result = await conn.execute("DELETE FROM books WHERE id = $1", book_id)
        return {"status": "success" if result == "DELETE 1" else "not_found"}


async def get_books_from_db(pool, offset: int = 0, limit: int = 10):
    """Получаю список книг с пагинацией
    
    offset-сколько пропустить, limit-сколько вернуть
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM books OFFSET $1 LIMIT $2", offset, limit)
        return [dict(row) for row in rows]