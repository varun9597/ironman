from flask import jsonify, request, session
import bcrypt
from sqlalchemy.orm import sessionmaker
from models.user import User
from database import get_engine

def sign_in():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session_db = Session()

    try:
        user = session_db.query(User).filter(User.username == username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.user_id
            return jsonify({'message': 'Login Success!', 'user_id': user.user_id}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred while signing in'}), 500
    finally:
        session_db.close()
