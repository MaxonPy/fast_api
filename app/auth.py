import jwt
from aiohttp import web
from datetime import datetime, timezone, timedelta
from app.config import SECRET_KEY, ALGORITHM



def create_access_token(data: dict):
    """Создаю JWT токен для пользователя
    
    Токен живет 30 минут, потом нужно перелогиниться
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def token_required(handler):
    """Декоратор для защиты роутов
    
    Проверяю токен в заголовке. Если нет или невалидный - 401
    """

    def wrapper(request):
        token = request.headers.get("Авторизация")
        if not token:
            raise web.HTTPUnauthorized(text="токен не найден")
        try:
            payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
            request["user"] = payload
        except jwt.ExpiredSignatureError:
            raise web.HTTPUnauthorized(text="токен просрочен")
        except jwt.InvalidTokenError:
            raise web.HTTPUnauthorized(text="невалидный токен")

        return handler(request)

    return wrapper
