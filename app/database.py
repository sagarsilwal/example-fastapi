from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<db_name>'
#SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:sagar@localhost:5432/fastapi'
 
#use env variable
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


#create engine which is responsible for sqlalchemy to connect to postgresql db
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#create session to talk to db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#the function declarative_base() that returns a class
Base = declarative_base()


#create dependency to connect to db or get a session to db
#evertime we get request we get a session, we are going to sense SQl statements to it
#after the request we close it out
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

#for database connection
#while True: 

#  try:
#    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#    password='sagar', cursor_factory=RealDictCursor)

    #open a cursor to perform database operation
#    cursor = conn.cursor()
#    print("Database Connection is Successful!")
#    break

#  except Exception as error:
#    print("Database Connection Failed!")
#    print("Error: ", error)
#    time.sleep(2)
