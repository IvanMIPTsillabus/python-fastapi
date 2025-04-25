import argon2
import jwt
from app.core.config import SECRET_KEY, JWT_ALGO

password_hasher = argon2.PasswordHasher()


def hash_password(password):
    return password_hasher.hash(password)


def verify_password(hashed_password, password):
    try:
        return password_hasher.verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        return False


def create_access_token(payload):
    try:
        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGO)
        return token
    except jwt.PyJWTError as e:
        print(f"Ошибка при создании токена доступа. Подробнее: {e}")
        return None


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGO])
        user_id: str = payload.get("user_id")
        return user_id
    except jwt.PyJWTError as e:
        print(f"Ошибка при декодирования токена доступа. Подробнее: {e}")
        return None
