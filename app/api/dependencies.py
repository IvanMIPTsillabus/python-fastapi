from app.database.session import Database
from app.dotnetparser.dnp import DotNetParser
from app.core.config import (DATABASE_PATH,
                             DATABASE_SCHEMA)


def get_database_session() -> Database:
    db = Database(DATABASE_PATH, DATABASE_SCHEMA)
    db.create()
    try:
        yield db
    finally:
        db.close_connection()


def get_parser() -> DotNetParser:
    return DotNetParser()
