from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

sql_url = os.getenv('SQL_URL')

def get_connection():
    engine = create_engine(sql_url, isolation_level="AUTOCOMMIT")
    conn = engine.connect()
    return conn

def get_engine():
    engine = create_engine(sql_url, isolation_level="AUTOCOMMIT")
    return engine

# con = get_connection()
# con.execute(text("INSERT INTO users (name, username, password) VALUES ('varun', 'varun', 'varun')"))
# result = con.execute(text("select * from users")).fetchall()
# print(result)
