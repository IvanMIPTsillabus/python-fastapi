import datetime
import sqlite3

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_database_session
from app.core.config import ACCESS_TOKEN_EXPIRE_HOURS
from app.core.security import create_access_token, verify_password, hash_password
from app.models.auth import UserRegistrationData, UserRegistrationResponse

router = APIRouter()


@router.post("/login")
def auth(user_data: OAuth2PasswordRequestForm = Depends(), database: sqlite3.Connection = Depends(get_database_session)):
    _, user_id = database.get_user_id(user_data.username)
    if user_id:
        result = database.get_user_info(user_id)
        if result:
            if verify_password(result[1], user_data.password):
                payload = {
                    "user_id": user_id,
                    "name": result[2],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
                }
                access_token = create_access_token(payload)
                if access_token:
                    return {"access_token": access_token,
                            "token_type": "bearer"}
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": "Внутренняя ошибка при авторизации пользователя"}
                )
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Неверный пароль"}
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Внутренняя ошибка при авторизации пользователя"}
            )
    else:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Пользователь не зарегистрирован"}
        )


@router.post("/register")
def register(user_data: UserRegistrationData, database: sqlite3.Connection = Depends(get_database_session)):
    is_user_created, _ = database.get_user_id(user_data.login)
    if not is_user_created:
        result, user_id = database.add_user(user_data.login, hash_password(user_data.password), user_data.name)
        if result:
            return UserRegistrationResponse(id=user_id)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Внутренняя ошибка при регистрации пользователя"}
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Пользователь уже зарегистрирован"}
    )
