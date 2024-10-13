from flask import jsonify, request, session
import bcrypt
from sqlalchemy.orm import sessionmaker
from models.user import User
from database import get_engine
from flask_jwt_extended import create_access_token
from helpers.db_helper import get_session_db
from datetime import timedelta

def sign_in():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    session_db = get_session_db()

    try:
        user = session_db.query(User).filter(User.username == username).first()
        print(user)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # session['user_id'] = user.user_id
            access_token = create_access_token(identity={'user_id': user.user_id, 'role': user.role}, expires_delta=timedelta(hours=24))
            print("User ID stored in JWT:", access_token)  # Debugging
            return jsonify({'message': 'Login Success!', 'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred while signing in'}), 500
    finally:
        session_db.close()
