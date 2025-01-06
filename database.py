from sqlmodel import create_engine, Session, SQLModel
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
