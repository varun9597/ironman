from flask import Blueprint
from controllers.society_controller import fetch_society_list_con
from flask_jwt_extended import jwt_required, get_jwt_identity

society_bp = Blueprint('society', __name__)

@society_bp.route("/api/fetch_society_list", methods=['GET'])
@jwt_required()
def fetch_society_list():
    print("inside Fetch Society List Route")
    return fetch_society_list_con()
