from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import logging
import time

logger = logging.getLogger(__name__)
load_dotenv()

db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")

if not all([db_host, db_port, db_name, db_user, db_password]):
    raise ValueError("Missing required database configuration")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Number of connections to maintain
    max_overflow=10,  # Additional connections beyond pool_size
    echo=False,  # Set to True for SQL query logging (useful for debugging)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def wait_for_db(max_retries=30, retry_interval=1):
    """Wait for database to be ready. Useful for Docker environments."""
    for i in range(max_retries):
        try:
            conn = engine.connect()
            conn.close()
            logger.info("Database connection successful")
            return True
        except Exception as e:
            if i < max_retries - 1:
                logger.warning(f"Database not ready, retrying in {retry_interval}s... ({i+1}/{max_retries})")
                time.sleep(retry_interval)
            else:
                logger.error(f"Failed to connect to database after {max_retries} attempts: {e}")
                raise
    return False