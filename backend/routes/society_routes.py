from flask import Blueprint
from controllers.society_controller import fetch_society_list_con , fetch_society_details_con
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


