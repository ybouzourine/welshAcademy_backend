from flask import Blueprint, jsonify, request, Response

from db import db
from models.ingredient import Ingredient
from models.user import User, Role

#http://127.0.0.1:5000/admin/ingredients/create?ingredientname=tomate
#http://127.0.0.1:5000/admin/ingredients/update?ingredientid=1&newname=huile
#http://127.0.0.1:5000/ingredients/delete?ingredientid=1


# """ INGREDIENTS """
admin_ingredient_bp = Blueprint("admin_ingredient", __name__, url_prefix="/admin/ingredients")

@admin_ingredient_bp.route('/create', methods=['GET' , 'POST'])
def create_ingredient():
    ingredient_name= request.args.get('ingredientname')

    if not Ingredient.query.filter(Ingredient.name == ingredient_name).first():
        new_ingredient = Ingredient(name=ingredient_name)
        db.session.add(new_ingredient)
        db.session.commit()
        return "Ingredient created "
    else:
        return "Ingredient exists already"

# @admin_ingredient_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
# def delete_ingredient():
#     ingredient_id = request.args.get('ingredientid')
#     #ingredient = get_ingredient_by_id(ingredient_id)
#     ingredient = Ingredient.query.filter(Ingredient.id == ingredient_id).first()
#     if not ingredient:
#       return 'Can\'t delete ingredient. The ingredient does not exist'
#     else:
#         #delete_ingredient(ingredient)
#         db.session.delete(ingredient)
#         db.session.commit()
#         return 'Ingredient deleted successfully'
#
# @admin_ingredient_bp.route('/update', methods=['GET' , 'POST'])
# def update_ingredient():
#     ingredient_id = request.args.get('id')
#     ingredient_new_name = request.args.get('newname')
#
#     ingredient = Ingredient.query.filter(Ingredient.id == ingredient_id).first()
#     #ingredient = get_ingredient_by_id(ingredient_id)
#     if not ingredient:
#         return 'The ingredient doest not exist'
#     else:
#         #update_ingredient(ingredient_id,new_ingredient_name)
#         if ingredient.name != ingredient_new_name:
#             ingredient.name = ingredient_new_name
#             db.session.commit()
#         return 'Ingredient updated successfully'
#
# """                          A FAIIIIIIIIIIIIIIIIIIIIRE """
# @admin_ingredient_bp.route('/ingredients', methods=['GET' , 'POST'])
# def getall_ingredient():
#     if not Ingredient.query.all():
#         return  "No ingredients in the db"
#     else:
#         # #ist_ingredients = Ingredient.query().all()
#         return "Ingredients list "
#
#         """                          A FAIIIIIIIIIIIIIIIIIIIIRE """
#
#
# """ USERS """
# #http://127.0.0.1:5000/admin/users/create?username=youcef&email=youcefdaicine&password=lesgroupe&roleid=2
# #http://127.0.0.1:5000/admin/ingredients/update?ingredientid=1&newname=huile
# #http://127.0.0.1:5000/admin/ingredients/delete?ingredientid=1
#
# # user_name= request.args.get('username')
# #     email = request.args.get('email')
# #     password = request.args.get('password')
# #     role = request.args.get('role')
#
admin_user_bp = Blueprint("admin_user", __name__, url_prefix="/admin/users")
#
# @admin_user_bp.route('/getall', methods=['GET'])
# def getall_user():
#     if not Ingredient.query.all():
#         return "No users in the db"
#     else:
#         #ist_ingredients = Ingredient.query().all()
#         return "Users list "
#
@admin_user_bp.route('/create', methods=['GET' , 'POST'])
def create_user():
    username= request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    role_id = request.args.get('roleid')

    if not User.query.filter(User.username == username).first():
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return "User created "
    else:
        return "Ingredient exists already"
#
# @admin_user_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
# def delete_user():
#     user_id = request.args.get('userid')
#     #ingredient = get_ingredient_by_id(ingredient_id)
#     user = User.query.filter(User.id == user_id).first()
#     if not user:
#       return 'Can\'t delete ingredient. The ingredient does not exist'
#     else:
#         #delete_ingredient(ingredient)
#         db.session.delete(user)
#         db.session.commit()
#         return 'Ingredient deleted successfully'
#
@admin_user_bp.route('/update/name', methods=['GET' , 'POST'])
def update_username():
    user_id = request.args.get('id')
    user_new_name = request.args.get('newname')

    #ingredient = get_ingredient_by_id(ingredient_id)
    if not User.query.filter(User.id == user_id).first():
        return 'The User doest not exist'
    else:
        user = User.query.filter(User.id == user_id).first()
        #update_ingredient(ingredient_id,new_ingredient_name)
        if user.username != user_new_name:
            user.username = user_new_name
            db.session.commit()
        return 'User updated successfully'

@admin_user_bp.route('/update/email', methods=['GET' , 'POST'])
def update_email():
    user_id = request.args.get('id')
    user_new_email = request.args.get('newemail')

    #ingredient = get_ingredient_by_id(ingredient_id)
    if not User.query.filter(User.id == user_id).first():
        return 'The User doest not exist'
    else:
        user = User.query.filter(User.id == user_id).first()
        #update_ingredient(ingredient_id,new_ingredient_name)
        if user.email != user_new_email:
            user.email = user_new_email
            db.session.commit()
        return 'User updated successfully'

@admin_user_bp.route('/update/password', methods=['GET' , 'POST'])
def update_password():
    user_id = request.args.get('id')
    new_password = request.args.get('newpassword')

    #ingredient = get_ingredient_by_id(ingredient_id)
    if not User.query.filter(User.id == user_id).first():
        return 'The User doest not exist'
    else:
        user = User.query.filter(User.id == user_id).first()
        #update_ingredient(ingredient_id,new_ingredient_name)
        if user.password != new_password:
            user.password = new_password
            db.session.commit()
        return 'User updated successfully'

@admin_user_bp.route('/delete', methods=['GET'])
def delete_user():
    user_id = request.args.get('id')

    #ingredient = get_ingredient_by_id(ingredient_id)
    if not User.query.filter(User.id == user_id).first():
        return 'The User doest not exist'
    else:
        user = User.query.filter(User.id == user_id).first()
        #update_ingredient(ingredient_id,new_ingredient_name)
        db.session.delete(user)
        db.session.commit()
        return 'User updated successfully'

# """ RECIPES """

"""Roles"""
# http://127.0.0.1:5000/admin/roles/create?rolename=user

admin_role_bp = Blueprint("admin_role", __name__, url_prefix="/admin/roles")


@admin_role_bp.route('/create', methods=['GET' , 'POST'])
def create_role():
    role_name = request.args.get('rolename')
    if not Role.query.filter(Role.role_name == role_name).first():
        new_role = Role(role_name=role_name)
        db.session.add(new_role)
        db.session.commit()
        return "New role created "
    else:
        return "Role exists already"
    # return "hello"