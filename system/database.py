from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

Base = declarative_base()

# PostgreSQL database URL
SQLALCHEMY_DATABASE_URL = "postgresql://fukuro:fukuro@localhost/fukurodb"

# Create engine with echo for debugging (no need for connect_args for PostgreSQL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True  # Enable SQL logging for debugging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database with all required tables."""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info(f"Database initialized at: {SQLALCHEMY_DATABASE_URL}")
        # Test the connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()
        logger.info("Database connection test successful")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        logger.exception("Full traceback:")
        raise

def get_db():
    """Database session dependency that ensures proper session closure."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
