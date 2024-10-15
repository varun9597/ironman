from flask import jsonify, request, session
from models.user import User
from helpers.db_helper import get_session_db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.society import Society
from sqlalchemy import and_
from helpers.password_helper import generate_default_password

def fetch_user_list_con(db):
    current_user = get_jwt_identity()
    print("Current User is -->", current_user)
    user_id = current_user['user_id']

    try:
        users = db.query(User.user_id, User.name, User.role).filter(and_(User.is_active == 'Y')).order_by(User.name).all()
        user_data = [{'user_id' : item[0], 'name' : item[1], 'role' : item[2]} for item in users]  #[item[0] for item in societies]
        return jsonify({'message': "List of Users", 'data': user_data})    
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred while fetching society list'}), 500
    finally:
        db.close()

def fetch_user_details_con(db,user_id):
    current_user = get_jwt_identity()
    print("Current User is -->", current_user)
    current_user_id = current_user['user_id']

    try:
        users = db.query(User.name, User.username, User.role).\
                filter(and_(User.user_id == user_id)).first()
        user_data = {'name' : users.name, 'username' : users.username, 'role' : users.role}
        print("User Data -->",user_data)
        return jsonify({'message': "User Detail", 'data': user_data})    
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred while fetching user info'}), 500
    finally:
        db.close() 

def edit_user_info_con(db, user_id, new_name, new_role):
    current_user = get_jwt_identity()
    print("Current User is -->", current_user)
    current_user_id = current_user['user_id']
    if not user_id or not new_name or not new_role:
        return jsonify({"error" : "user_id and name or role are required"}), 400
    try:
        user = db.query(User).filter(and_(User.user_id == user_id, User.is_active == 'Y')).first()
        if user:
            user.name = new_name
            user.role = new_role
            db.commit()
            return jsonify({"message": "User updated successfully"}), 200
        return jsonify({"error": "Failed to update user"}), 500  
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred while Editing user'}), 500
    finally:
        db.close()  

def delete_user_con(db, user_id) :
    current_user = get_jwt_identity()
    print("Current User is -->", current_user)
    current_user_id = current_user['user_id']
    if not user_id :
        return jsonify({"error" : "user_id is required"}), 400
    try:
        user = db.query(User).filter(and_(User.user_id == user_id, User.is_active == 'Y')).first()
        if user:
            # print(society.soc_name)
            user.is_active = "N"
            db.commit()
            return jsonify({"message": "User deleted successfully"}), 200
        return jsonify({"error": "Failed to delete user"}), 500  
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred while Deleting User'}), 500
    finally:
        db.close()

def add_user_con(db, user_name, user_role, username) :
    current_user = get_jwt_identity()
    print("Current User is -->", current_user)
    current_user_id = current_user['user_id']
    if not user_name or not user_role or not username :
        return jsonify({"error" : "user_name, user_role and username is required"}), 400
    try:
        existing_user = db.query(User).filter(and_(User.username == username)).first()
        if existing_user:
            return jsonify({"error": "User Already Exists"}), 400
        
        new_user = User(
            username = username,
            name = user_name,
            role = user_role,
            password = generate_default_password(),
            is_active = 'Y'
        )
        db.add(new_user)
        db.commit()
        return jsonify({"message": "User Added Successfully", 'user_id': new_user.user_id}), 201  
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred while Adding User'}), 500
    finally:
        db.close()

def reset_password_con(db, user_id) :
    current_user = get_jwt_identity()
    print("Current User is -->", current_user)
    current_user_id = current_user['user_id']
    if not user_id :
        return jsonify({"error" : "user_id is required"}), 400
    try:
        existing_user = db.query(User).filter(and_(User.user_id == user_id)).first()
        if not existing_user:
            return jsonify({"error": "User Does not Exists"}), 400
        existing_user.password = generate_default_password()        
        db.commit()
        return jsonify({"message": "Password Reset Successfully"}), 201  
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred while Resetting Password for User'}), 500
    finally:
        db.close()

