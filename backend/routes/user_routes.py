from flask import Blueprint, request
from controllers.user_controller import fetch_user_list_con , fetch_user_details_con, edit_user_info_con, delete_user_con, add_user_con, reset_password_con
from flask_jwt_extended import jwt_required, get_jwt_identity
from helpers.db_helper import get_session_db

users_bp = Blueprint('user', __name__)

session_db = get_session_db()

@users_bp.route("/api/fetch_user_list", methods=['GET'])
@jwt_required()
def fetch_user_list():
    print("inside Fetch User List Route")
    return fetch_user_list_con(session_db)


@users_bp.route("/api/view_user/<int:user_id>", methods=['GET'])
@jwt_required()
def fetch_user_details(user_id):
    print("inside Fetch User Details Route")
    return fetch_user_details_con(session_db,user_id)

@users_bp.route("/api/edit_user", methods=['POST'])
@jwt_required()
def edit_user_info():
    print("inside Edit User Info Route")
    data = request.get_json()
    user_id = data.get('user_id')
    new_name = data.get('name')
    new_role = data.get('role')
    return edit_user_info_con(session_db, user_id, new_name, new_role)

@users_bp.route("/api/delete_user", methods=['POST'])
@jwt_required()
def delete_user():
    print("inside Delete User Route")
    data = request.get_json()
    user_id = data.get('user_id')
    return delete_user_con(session_db,user_id)

@users_bp.route("/api/add_user", methods=['POST'])
@jwt_required()
def add_user():
    print("inside Add User Route")
    data = request.get_json()
    user_name = data.get('user_name')
    user_role = data.get('user_role')
    username = data.get('username')
    return add_user_con(session_db,user_name, user_role, username)

@users_bp.route("/api/reset_password", methods = ['POST'])
@jwt_required()
def reset_password():
    print("Inside Reset password Route")
    data = request.get_json()
    user_id = data.get('user_id')
    return reset_password_con(session_db, user_id)


