from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.paths import get_db_path
from app.models.base import Base

logger = logging.getLogger(__name__)


def _sqlite_engine() -> Engine:
    db_path = get_db_path()
    url = f"sqlite+pysqlite:///{db_path.as_posix()}"
    engine = create_engine(
        url,
        future=True,
        echo=False,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine, "connect")
    def _set_sqlite_pragmas(dbapi_connection, connection_record):  # type: ignore[no-redef]
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.close()

    return engine


engine = _sqlite_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    # Importa modelos para registrar as tabelas no metadata
    from app.models.activity import Activity  # noqa: F401
    from app.models.setting import Setting  # noqa: F401
    from app.models.vehicle import Vehicle  # noqa: F401

    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)
    logger.info("Banco inicializado em %s", db_path)


@contextmanager
def session_scope() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
