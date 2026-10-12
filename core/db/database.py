"""Local SQLite engine and session-factory helpers."""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from core.db.models import Base


def create_sqlite_engine(database_path: str | Path) -> Engine:
    """Create a SQLite engine with foreign-key enforcement enabled."""
    path = str(database_path)
    if path == ":memory:":
        url = "sqlite+pysqlite:///:memory:"
    else:
        resolved_path = Path(path)
        resolved_path.parent.mkdir(parents=True, exist_ok=True)
        url = f"sqlite+pysqlite:///{resolved_path}"

    engine = create_engine(
        url,
        connect_args={"check_same_thread": False},
        future=True,
    )

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection: object, _connection_record: object) -> None:
        cursor = dbapi_connection.cursor()  # type: ignore[union-attr]
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Return a unit-of-work factory with objects available after commit."""
    return sessionmaker(bind=engine, expire_on_commit=False)


def initialize_database(engine: Engine) -> None:
    """Create the Stage 2 local tables if they do not already exist."""
    Base.metadata.create_all(engine)
