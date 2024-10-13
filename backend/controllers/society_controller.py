from flask import jsonify, request, session
from models.user import User
from helpers.db_helper import get_session_db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.society import Society
from sqlalchemy import and_

def fetch_society_list_con(db):
    current_user = get_jwt_identity()
    print("Current User is -->", current_user)
    user_id = current_user['user_id']

    try:
        societies = db.query(Society.society_id, Society.soc_name).filter(and_(Society.is_active == 'Y', User.user_id == user_id, User.is_active == 'Y')).order_by(Society.soc_name).all()
        society_data = [{'society_id' : item[0], 'society_name' : item[1]} for item in societies]  #[item[0] for item in societies]
        return jsonify({'message': "List of societies", 'data': society_data})    
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred while fetching society list'}), 500
    finally:
        db.close()

def fetch_society_details_con(db,society_id):
    current_user = get_jwt_identity()
    print("Current User is -->", current_user)
    user_id = current_user['user_id']

    try:
        societies = db.query(Society.society_id, Society.soc_name, User.name).\
                    join(User, User.user_id == Society.user_id).\
                    filter(and_(Society.is_active == 'Y', Society.society_id == society_id)).first()
        society_data = {'society_id' : societies.society_id, 'society_name' : societies.soc_name, 'username' : societies.name}
        print("Soc Data -->",society_data)
        return jsonify({'message': "Society Detail", 'data': society_data})    
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred while fetching society list'}), 500
    finally:
        db.close()    

