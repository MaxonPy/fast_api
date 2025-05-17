import pytest
from app.models import Book
from app.db import add_book_to_db, delete_book_from_db, get_books_from_db


@pytest.mark.asyncio
async def test_add_book_to_db(mocker):
    pool = mocker.MagicMock()
    conn = mocker.AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = conn
    mock_result = {"id": 1, "title": "Test Book", "author": "Author", "year": 2021, "isbn": "1234567890123"}
    conn.fetchrow.return_value = mock_result
    book = Book(title="Test Book", author="Author", year=2021, isbn="1234567890123")
    result = await add_book_to_db(pool, book)
    assert result == mock_result
    conn.fetchrow.assert_called_once_with(
        "INSERT INTO books (title, author, year, isbn) VALUES ($1, $2, $3, $4) RETURNING *",
        book.title, book.author, book.year, book.isbn
    )

@pytest.mark.asyncio
async def test_delete_book_from_db(mocker):
    pool = mocker.MagicMock()
    conn = mocker.AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = conn
    conn.execute.return_value = "DELETE 1"
    result = await delete_book_from_db(pool, 2)
    assert result == {"status": "success"}
    conn.execute.assert_called_once_with("DELETE FROM books WHERE id = $1", 2)

@pytest.mark.asyncio
async def test_get_books_from_db(mocker):
    pool = mocker.MagicMock()
    conn = mocker.AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = conn
    mock_rows = [
        {"id": 1, "title":   "Test Book 1", "author": "Author 1", 
         "year": 2021, "isbn": "1234567890123"},
        {"id": 2,  "title": "Test Book 2", "author": "Author 2",
          "year": 2020, "isbn": "1234567890124"}]
    conn.fetch.return_value = mock_rows

    result = await get_books_from_db(pool, offset=0, limit=2)
    assert result == mock_rows
