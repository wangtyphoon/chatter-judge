import time
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

from .connection import engine

__all__ = ["Base", "User", "init_models"]

CONNECT_TIMEOUT = 20

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, nullable=False
    )
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)


async def init_models() -> None:
    for _ in range(CONNECT_TIMEOUT):
        try:
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)
            return
        except OSError:
            time.sleep(1)
