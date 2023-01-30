from flask import Blueprint, jsonify, request, Response, flash

from db import db
from models import recipe
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.recipeingredient import RecipeIngredient
#
recipe_bp = Blueprint("recipes", __name__, url_prefix="/recipes")
#
#http://127.0.0.1:5000/recipes/create?recipename=omelette&recipedescription=melangeomeletteavecfromage&ingredients=1&ingredients=2&ingredients=3&quantity=gr&quantity=br&quantity=fr

# #http://127.0.0.1:5000/recipes/update?previousname=omelette&newname=pizza&newrecipedescription=tomateetolives
# #http://127.0.0.1:5000/recipes/delete?recipename=pizza
#
def get_ingredient_by_id(ingredient_id):
    ingredient = Ingredient.query.filter(
        Ingredient.id == ingredient_id).first()
    return ingredient

def get_recipe_by_id(recipe_id):
    ingredient = Ingredient.query.filter(
        Ingredient.id == recipe_id).first()
    return ingredient

@recipe_bp.route('/create', methods=['GET' , 'POST'])
def create_recipe():
    recipe_name= request.args.get('recipename')
    recipe_description=request.args.get('recipedescription')
    recipe_ingredients_id=request.args.getlist('ingredients')
    quantities=request.args.getlist('quantity')

    if not Recipe.query.filter(Recipe.name == recipe_name).first():
        new_recipe = Recipe(name=recipe_name, description=recipe_description)
        db.session.add(new_recipe)
        db.session.commit()
        if Recipe.query.filter(Recipe.name == recipe_name).first():
            recipe_id=new_recipe.id
            for i in range(len(recipe_ingredients_id)):
                recipeingredients = RecipeIngredient(quantity=quantities[i],recipe_id=recipe_id, ingredient_id=recipe_ingredients_id[i])
                db.session.add(recipeingredients)
                db.session.commit()
            return 'recipe created'
    else:
        'recipe exists already '


@recipe_bp.route('/delete', methods=['GET' , 'POST'])
def delete_recipe():
    recipe_name = request.args.get('recipename')

    recipe = Recipe.query.filter(
            Recipe.name==recipe_name).first()
    if not recipe:
      return 'The recipe doest not exixst'
    else:
        db.session.delete(recipe)
        db.session.commit()
        return 'Recipe deleted'


# @recipe_bp.route('/update', methods=['GET' , 'POST'])
# def update_recipe():
#     previous_recipe_name = request.args.get('previousname')
#     new_recipe_name = request.args.get('newname')
#     new_recipe_description=request.args.get('newrecipedescription')
#
#     recipe = Recipe.query.filter(
#         Recipe.name == previous_recipe_name).first()
#     if not recipe:
#       return 'The recipe doest not exixst'
#     else:
#         if previous_recipe_name!=new_recipe_name:
#             recipe.name = new_recipe_name
#         if recipe.description != new_recipe_description:
#             recipe.description = new_recipe_description
#         db.session.commit()
#         return 'Recipe updated'
#
# @recipe_bp.route('/update', methods=['GET' , 'POST'])
# def update_recipe_name():
#     previous_recipe_name = request.args.get('previousname')
#     new_recipe_name = request.args.get('newname')
#
#     recipe = Recipe.query.filter(
#         Recipe.name == previous_recipe_name).first()
#     if not recipe:
#       return 'The recipe doest not exixst'
#     else:
#         recipe.name= new_recipe_name
#         db.session.commit()
#         return 'Recipe name updated'
#
#
# @recipe_bp.route('/update', methods=['GET' , 'POST'])
# def update_recipe_description():
#     previous_recipe_name = request.args.get('previousname')
#     new_recipe_description = request.args.get('newrecipedescription')
#
#     recipe = Recipe.query.filter(
#         Recipe.name == previous_recipe_name).first()
#     if not recipe:
#       return 'The recipe doest not exixst'
#     else:
#         recipe.description=new_recipe_description
#         db.session.commit()
#         return 'Recipe descrition updated'