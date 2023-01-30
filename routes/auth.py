from flask_login import UserMixin, login_required, login_user, LoginManager, logout_user, current_user

from flask import Blueprint, jsonify, request, Response, redirect

from db import db
from models.user import User, Role

auth_bp = Blueprint("auth", __name__, url_prefix="/")

login_manager = LoginManager()

#http://127.0.0.1:5000/login/register?username=youcef&email=youcef@hey.com&password=you&role=user
@auth_bp.route('/register', methods=['GET' , 'POST'])
def register():
    username= request.args.get('username')
    email=request.args.get('email')
    password=request.args.get('password')
    role=request.args.get('role')

    if not User.query.filter(User.email == email).first():
        new_user = User(name=username, password=password, email=email)
        new_user.role.append(Role(role=role))
        db.session.add(new_user)
        db.session.commit()

    return "register "

# @auth_bp.route('login', methods=['GET' , 'POST'])
# def register():
#     email=request.args.get('email')
#     password=request.args.get('password')
#
#     user = User.query.filter(
#             User.email == email,
#             User.password==password).first()
#
#     if not user:
#       return redirect('/register')
#     else:
#         login_user(user)
#         return f'Logged in {user.role}'
#
# @auth_bp.route('/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#     logout_user()
#     return "Logged out "
#
