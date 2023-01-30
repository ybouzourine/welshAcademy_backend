from flask import Blueprint, jsonify, request, Response

from db import db
from models.ingredient import Ingredient
from models.user import User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")



""" INGREDIENTS """

@admin_bp.route('/ingredient/create', methods=['GET' , 'POST'])
def create_ingredient():
    ingredient_name= request.args.get('ingredientname')

    if not Ingredient.query.filter(Ingredient.name == ingredient_name).first():
        new_ingredient = Ingredient(name=ingredient_name)
        db.session.add(new_ingredient)
        db.session.commit()
        return "Ingredient created "
    else:
        return "Ingredient exists already"

@admin_bp.route('/ingredient/delete/<int:id>', methods=['GET', 'POST'])
def delete_ingredient():
    ingredient_id = request.args.get('ingredientid')
    #ingredient = get_ingredient_by_id(ingredient_id)
    ingredient = Ingredient.query.filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
      return 'Can\'t delete ingredient. The ingredient does not exist'
    else:
        #delete_ingredient(ingredient)
        db.session.delete(ingredient)
        db.session.commit()
        return 'Ingredient deleted successfully'

@admin_bp.route('/update', methods=['GET' , 'POST'])
def update_ingredient():
    ingredient_id = request.args.get('id')
    ingredient_new_name = request.args.get('newname')

    ingredient = Ingredient.query.filter(Ingredient.id == ingredient_id).first()
    #ingredient = get_ingredient_by_id(ingredient_id)
    if not ingredient:
        return 'The ingredient doest not exist'
    else:
        #update_ingredient(ingredient_id,new_ingredient_name)
        if ingredient.name != ingredient_new_name:
            ingredient.name = ingredient_new_name
            db.session.commit()
        return 'Ingredient updated successfully'

"""                          A FAIIIIIIIIIIIIIIIIIIIIRE """
@admin_bp.route('/ingredients', methods=['GET' , 'POST'])
def getall_ingredient():
    if not Ingredient.query.all():
        return  "No ingredients in the db"
    else:
        # #ist_ingredients = Ingredient.query().all()
        return "Ingredients list "

        """                          A FAIIIIIIIIIIIIIIIIIIIIRE """


""" RECIPES """





""" USERS """

@admin_bp.route('/users', methods=['GET'])
def getall_user():
    if not Ingredient.query.all():
        return "No users in the db"
    else:
        #ist_ingredients = Ingredient.query().all()
        return "Users list "

@admin_bp.route('/user/create', methods=['GET' , 'POST'])
def create_user():
    user_name= request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    role = request.args.get('role')

    if not Ingredient.query.filter(User.name == user_name).first():
        new_user = User()
        db.session.add(new_user)
        db.session.commit()
        return "Ingredient created "
    else:
        return "Ingredient exists already"

@admin_bp.route('/ingredient/delete/<int:id>', methods=['GET', 'POST'])
def delete_ingredient():
    ingredient_id = request.args.get('ingredientid')
    #ingredient = get_ingredient_by_id(ingredient_id)
    ingredient = Ingredient.query.filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
      return 'Can\'t delete ingredient. The ingredient does not exist'
    else:
        #delete_ingredient(ingredient)
        db.session.delete(ingredient)
        db.session.commit()
        return 'Ingredient deleted successfully'

@admin_bp.route('/update', methods=['GET' , 'POST'])
def update_ingredient():
    ingredient_id = request.args.get('id')
    ingredient_new_name = request.args.get('newname')

    ingredient = Ingredient.query.filter(Ingredient.id == ingredient_id).first()
    #ingredient = get_ingredient_by_id(ingredient_id)
    if not ingredient:
        return 'The ingredient doest not exist'
    else:
        #update_ingredient(ingredient_id,new_ingredient_name)
        if ingredient.name != ingredient_new_name:
            ingredient.name = ingredient_new_name
            db.session.commit()
        return 'Ingredient updated successfully'


