from flask import Blueprint, request
from controllers.society_controller import fetch_society_list_con , fetch_society_details_con, edit_society_info_con, delete_society_con, add_society_con
from flask_jwt_extended import jwt_required, get_jwt_identity
from helpers.db_helper import get_session_db

society_bp = Blueprint('society', __name__)

session_db = get_session_db()

@society_bp.route("/api/fetch_society_list", methods=['GET'])
@jwt_required()
def fetch_society_list():
    print("inside Fetch Society List Route")
    return fetch_society_list_con(session_db)


@society_bp.route("/api/view_society/<int:society_id>", methods=['GET'])
@jwt_required()
def fetch_society_details(society_id):
    print("inside Fetch Society List Route")
    return fetch_society_details_con(session_db,society_id)

@society_bp.route("/api/edit_society", methods=['POST'])
@jwt_required()
def edit_society_info():
    print("inside Edit Society Info Route")
    data = request.get_json()
    society_id = data.get('society_id')
    new_society_name = data.get('society_name')
    return edit_society_info_con(session_db, society_id, new_society_name)

@society_bp.route("/api/delete_society", methods=['POST'])
@jwt_required()
def delete_society():
    print("inside Delete Society Route")
    data = request.get_json()
    society_id = data.get('society_id')
    return delete_society_con(session_db,society_id)

@society_bp.route("/api/add_society", methods=['POST'])
@jwt_required()
def add_society():
    print("inside Add Society Route")
    data = request.get_json()
    society_name = data.get('society_name')
    return add_society_con(session_db,society_name)


