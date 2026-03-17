from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------
# DB PARTS
# ------------------------------------------

db_username = os.getenv("DB_USERNAME", "postgres")
db_password = os.getenv("DB_PASSWORD", "123456")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "research_platform")

# ------------------------------------------
# FINAL DATABASE URL
# ------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
)

# --------------------------------------------------
# Engine
# --------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    future=True
)

# --------------------------------------------------
# Session factory
# --------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# --------------------------------------------------
# Base model class
# --------------------------------------------------

Base = declarative_base()


# --------------------------------------------------
# Dependency for FastAPI routes
# --------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
