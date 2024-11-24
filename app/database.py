from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#if using manual sql instead of sqlalchemy
#import psycopg
#import time 
""" while True:
    try:
        conn = psycopg.connect(
            host="localhost",
            dbname='fastapi',
            user='postgres',
            password='Vainglory72#',
        )
        cursor = conn.cursor(row_factory=dict_row)#allow u to return value in a row format
        print("Database connected successfull!!!!")
        break

    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)
 """