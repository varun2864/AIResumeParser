import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine( #connection manager
    DATABASE_URL,
    echo = False
)

SessionLocal = sessionmaker( #one transaction scope
    bind = engine,
    autocommit = False, #mandates explicit commits
    autoflush = False #data only pushed when explicitly called
)


def get_session():
    session = SessionLocal()

    try:
        yield session
        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

