from flask import jsonify, request, session
from models.user import User
from helpers.db_helper import get_session_db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.society import Society
from sqlalchemy import and_

def fetch_society_list_con():
    current_user = get_jwt_identity()
    print("Current User is -->", current_user)
    user_id = current_user['user_id']

    session_db = get_session_db()

    try:
        societies = session_db.query(Society.soc_name).filter(and_(Society.is_active == 'Y', User.user_id == user_id, User.is_active == 'Y')).all()
        society_names = [item[0] for item in societies]
        return jsonify({'message': "List of societies", 'data': society_names})    
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred while fetching society list'}), 500
    finally:
        session_db.close()
    return current_user
    # data = request.get_json()
    # username = data.get('username')
    # password = data.get('password')

    # session_db = get_session_db()

    # try:
    #     user = session_db.query(User).filter(User.username == username).first()
    #     print(user)
    #     if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
    #         session['user_id'] = user.user_id
    #         return jsonify({'message': 'Login Success!', 'user_id': user.user_id, 'role':user.role}), 200
    #     else:
    #         return jsonify({'message': 'Invalid username or password'}), 401
    # except Exception as e:
    #     print("Error:", e)
    #     return jsonify({'error': 'An error occurred while signing in'}), 500
    # finally:
    #     session_db.close()
