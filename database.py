from sqlalchemy import create_engine, text
import os

sql_url = os.environ['SQL_URL']

def get_connection():
    engine = create_engine(sql_url, isolation_level="AUTOCOMMIT")
    conn = engine.connect()
    return conn

# con = get_connection()
# con.execute(text("INSERT INTO users (name, username, password) VALUES ('varun', 'varun', 'varun')"))
# result = con.execute(text("select * from users")).fetchall()
# print(result)
