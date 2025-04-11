from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import settings

# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# my_posts = [{"title": f"title of post {i}", "content": f"content post {i}", "id": (i-2)} for i in range(10,2,-1)]

# def find_post(id): 
#     for l in my_posts:
#         if l['id'] == id:
#             return l

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id']==id:
#             return i

# version 3
# import psycopg
# from psycopg.rows import dict_row

# while True:
#     try: 
#         conn = psycopg2.connect("host=localhost dbname=fastapi user=postgres password=postgres",
#                             #    row_factory=dict_row
#                             cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection wa s successful!")
#         break
#     except KeyboardInterrupt: 
#         print("Stopped by user")
#     except Exception as error:
#         print(f"Error connecting to database:\n\tError = {error}")
#         time.sleep(2)