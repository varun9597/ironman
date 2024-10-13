from sqlalchemy.orm import sessionmaker
from database import get_engine


def get_session_db():
    try:   
        engine = get_engine()
        Session = sessionmaker(bind=engine)
        session_db = Session()
    except Exception as e:
        print("Error in get_session-->",e)
        session_db = None
    finally:
        return session_db
    