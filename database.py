from sqlalchemy import create_engine, text

def get_connection():
    engine = create_engine("mysql+pymysql://u366979093_ironman:IronTest123@62.72.28.1/u366979093_ironmantest", isolation_level="AUTOCOMMIT")
    conn = engine.connect()
    return conn

# con = get_connection()
# con.execute(text("INSERT INTO users (name, username, password) VALUES ('varun', 'varun', 'varun')"))
# result = con.execute(text("select * from users")).fetchall()
# print(result)
