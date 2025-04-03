
# version 3
# import psycopg
# from psycopg.rows import dict_row
import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try: 
        conn = psycopg2.connect("host=localhost dbname=fastapi user=postgres password=postgres",
                            #    row_factory=dict_row
                            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection wa s successful!")
        break
    except KeyboardInterrupt: 
        print("Stopped by user")
    except Exception as error:
        print(f"Error connecting to database:\n\tError = {error}")
        time.sleep(2)