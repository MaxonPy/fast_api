import pytest
from unittest.mock import patch, AsyncMock


@pytest.mark.asyncio
async def test_login_success(client):
    """Тестирование успешного входа пользователя"""
    response = await client.post("/login", json={"username": "user", "password": "password"})
    assert response.status == 200
    data = await response.json()
    assert "access_token" in data
    assert isinstance(data["access_token"], str)  
    assert len(data["access_token"]) > 0  

@pytest.mark.asyncio
async def test_login_failure(client):
    """Тестирование неудачного входа пользователя"""

    response = await client.post("/login", json={"username": "wrong", "password": "password"})
    assert response.status == 401

@pytest.mark.asyncio
async def test_add_book(client, mock_access_token, mocker):
    """Тестирование добавления книги в базу данных """
    headers = {"Authorization": f"Bearer {mock_access_token}"}
    response = await client.post("/books", headers=headers, json={
        "title": "Test Book", "author": "Test Author",
        "year": 2021,
        "isbn": "1234567890123"
    })
    assert response.status == 200
    data = await response.json()
    assert data["id"] == 1
    assert data["title"] == "Test Book"

@pytest.mark.asyncio
async def test_get_books(client, mock_access_token, mocker):
    """Тестирование получения списка книг """
    mock_get_books_from_db = mocker.patch("app.db.get_books_from_db", return_value=[
        {"id": 1, "title": "Test Book", "author": "Author", "year": 2021, "isbn": "1234567890123"}
    ])
    headers = {"Authorization": f"Bearer {mock_access_token}"}
    response = await client.get("/books", headers=headers)
    assert response.status == 200
    data = await response.json()
    assert len(data["books"]) == 1

@pytest.mark.asyncio
async def test_delete_book(client, mock_access_token, mocker):
    """Тестирование удаления книги из базы данных"""
    headers = {"Authorization": f"Bearer {mock_access_token}"}
    response = await client.delete("/books/1", headers=headers)
    assert response.status == 200
    data = await response.json()
    assert data["status"] == "Book deleted successfully"

#

@pytest.mark.asyncio
async def test_add_book(client, mock_access_token):
    """Тестирование добавления новой книги"""
    new_book_data = {
        "title": "Тестовая книга", "author": "Имя Автора",
        "year": 2021, "isbn": "1234567890123"
    }
    headers = {
        "Authorization": f"Bearer {mock_access_token}"
    }
    # мок вызова к базе данных для добавления книги
    with patch("app.db.add_book_to_db", new_callable=AsyncMock) as mock_add_book:
        mock_add_book.return_value = {"id": 1, **new_book_data}  # симулирую успешное добавление
        response = await client.post("/books", json=new_book_data, headers=headers)
        assert response.status == 200
        response_data = await response.json()
        assert response_data["id"] == 1
        assert response_data["title"] == new_book_data["title"]
        assert response_data["author"] == new_book_data["author"]
