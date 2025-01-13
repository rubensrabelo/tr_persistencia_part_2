import sqlite3
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import event, Engine
from dotenv import load_dotenv
import os
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
