from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DB_USER ="postgres"
DB_PASSWORD = 12345
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "postgres"
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()