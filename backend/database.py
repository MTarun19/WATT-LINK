from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ==========================================================
# MySQL Database Configuration
# ==========================================================

DB_USERNAME = "root"
DB_PASSWORD = "mysql"      # <-- Replace with your MySQL password
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "watt_link"

DATABASE_URL = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================================================
# SQLAlchemy Engine
# ==========================================================

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

# ==========================================================
# Session Factory
# ==========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ==========================================================
# Base Model
# ==========================================================

Base = declarative_base()

# ==========================================================
# Dependency
# ==========================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()