from flask import Blueprint, jsonify, request, Response
from sqlalchemy import update

from db import db
from models import recipe
from models.ingredient import Ingredient
from models.recipe import Recipe

ingredient_bp = Blueprint("ingredients", __name__, url_prefix="/ingredients")

#http://127.0.0.1:5000/ingredients/create?ingredientname=tomate
#http://127.0.0.1:5000/ingredients/update?ingredientid=1&newname=huile
#http://127.0.0.1:5000/ingredients/delete?ingredientid=1


@ingredient_bp.route('/create', methods=['GET' , 'POST'])
def create_ingredient():
    ingredient_name= request.args.get('ingredientname')

    if not Ingredient.query.filter(Ingredient.name == ingredient_name).first():
        new_ingredient = Ingredient(name=ingredient_name)
        db.session.add(new_ingredient)
        db.session.commit()
        return "Ingredient created "
    else:
        return "Ingredient exists already"


@ingredient_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
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


@ingredient_bp.route('/update', methods=['GET' , 'POST'])
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
            #update_ingredient = update(Ingredient).values(name=ingredient_new_name)
            #db.session.execute(update_ingredient)
            db.session.commit()
        return 'Ingredient updated successfully'
