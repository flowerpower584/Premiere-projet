from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# SQLite local (par défaut) :
# sqlite:///./observatoire.db
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./observatoire.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # nécessaire pour SQLite avec FastAPI
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    class_=Session,
    future=True,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
