from flask import Blueprint
from controllers.auth_controller import sign_in

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/signin_auth", methods=['POST'])
def signin_route():
    print("inside Route")
    return sign_in()
