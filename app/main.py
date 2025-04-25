from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.parse import router as parsing_router
from app.api.user import router as user_router
from app.core.config import CORS_ORIGINS

app = FastAPI(
    title="Интеллектуальная система парсинга .NET-файлов.",
    version="1.0.0",
    contact={
        "name": "МФТИ",
        "url": "https://mipt.ru",
        "email": "digitaldepartments@mipt.ru",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    })

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(parsing_router, prefix="/parse", tags=["parse"])
