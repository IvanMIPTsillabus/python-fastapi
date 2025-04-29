import sqlite3

from fastapi import (APIRouter,
                     Depends,
                     status)
from fastapi.responses import JSONResponse

from app.api.dependencies import get_database_session
from app.core.security import OAUTH2_SCHEME
from app.core.security import (verify_password,
                               hash_password,
                               decode_token)
from app.models.user import (UserAuthLog,
                             UserPasswords,
                             UserResult)

router = APIRouter()


@router.post("/results")
def add_history(data: UserResult,
                token: str = Depends(OAUTH2_SCHEME),
                data_base: sqlite3.Connection = Depends(get_database_session)):
    user_id = decode_token(token)
    if user_id:
        data_base.add_user_result(user_id, data.data, data.timestamp)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Запись добавлена"}
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка"}
    )


@router.get("/results")
def get_history(token: str = Depends(OAUTH2_SCHEME),
                data_base: sqlite3.Connection = Depends(get_database_session)):
    user_id = decode_token(token)
    if user_id:
        results = data_base.get_user_results(user_id)
        if results:
            results_json = [UserResult(data=result[0], timestamp=result[1]) for result in results]
        else:
            results_json = []
        return results_json
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка"}
    )


@router.get("/me")
def get_user_info(token: str = Depends(OAUTH2_SCHEME),
                  data_base: sqlite3.Connection = Depends(get_database_session)):
    user_id = decode_token(token)
    if user_id:
        user_full_data = data_base.get_user_info(user_id)
        return {
            "username": user_full_data[0],
            "email": user_full_data[2]
        }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка"}
    )


@router.post("/auth_logs")
def add_auth_logs(log: UserAuthLog,
                  token: str = Depends(OAUTH2_SCHEME),
                  data_base: sqlite3.Connection = Depends(get_database_session)):
    user_id = decode_token(token)
    if user_id and data_base.add_user_auth_log(user_id, log.auth_at):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Запись о входе пользователя в систему добавлена"}
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка"}
    )


@router.get("/auth_logs")
def get_auth_logs(token: str = Depends(OAUTH2_SCHEME),
                  data_base: sqlite3.Connection = Depends(get_database_session)):
    user_id = decode_token(token)
    if user_id:
        logs = data_base.get_user_auth_logs(user_id)
        logs_json = [UserAuthLog(auth_at=log[0]) for log in logs]
        return logs_json
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка"}
    )


@router.delete("/delete_account")
def delete_account(token: str = Depends(OAUTH2_SCHEME),
                   data_base: sqlite3.Connection = Depends(get_database_session)):
    user_id = decode_token(token)
    if user_id and data_base.delete_user(user_id):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Аккаунт удален"}
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка"}
    )


@router.put("/change_password")
def change_password(passwords: UserPasswords,
                    token: str = Depends(OAUTH2_SCHEME),
                    data_base: sqlite3.Connection = Depends(get_database_session)):
    user_id = decode_token(token)
    if user_id:
        if verify_password(data_base.get_user_info(user_id)[1], passwords.old):
            if data_base.update_user_password(user_id, hash_password(passwords.new)):
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={"detail": "Пароль был изменен"}
                )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Внутренняя ошибка при смене пароля пользователя"}
            )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Неправильный старый пароль"}
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка при смене пароля пользователя"}
    )


@router.delete("/delete_results")
def delete_history(token: str = Depends(OAUTH2_SCHEME),
                   data_base: sqlite3.Connection = Depends(get_database_session)):
    user_id = decode_token(token)
    if user_id and data_base.delete_user_result(user_id):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Результаты удалены"}
        )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка"}
    )
