from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import settings

from models.base import Base

engine = create_engine(settings.database_url, echo=True)

def create_all_tables():
    """
    Creates all tables in the MySQL database using SQLAlchemy models.
    """
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully in MySQL.")

if __name__ == "__main__":
    create_all_tables()
