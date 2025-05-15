import pymysql
from sqlalchemy import create_engine, text
from settings import settings

def create_database():
    """
    Creates the MySQL database if it doesn't already exist.
    """
    try:
        engine = create_engine(settings.database_url, echo=True)
        with engine.connect() as connection:
            connection.execute(
                text(f"CREATE DATABASE IF NOT EXISTS {settings.db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            )
        print(f"Database '{settings.db_name}' created or already exists.")
    except Exception as e:
        print(f"Failed to create database: {e}")

if __name__ == "__main__":
    create_database()
