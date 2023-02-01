import numpy as numpy
from flask import Blueprint, jsonify, request, Response

from db import db
from models.favoriterecipe import FavoriteRecipe
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.recipeingredient import RecipeIngredient
from models.user import User
from repository.ingredient_repository import IngredientRepository
from repository.recipe_repository import RecipeRepository

"""                  INGREDIENTS                    """

user_ingredients_bp = Blueprint("users_ingredients", __name__, url_prefix="/user/ingredients")

# http://127.0.0.1:5000/user/ingredients/getall
@user_ingredients_bp.route('/getall', methods=['GET', 'POST'])
def getall_ingredients():
    if IngredientRepository.data_ingredient_is_empty():
        return 'The table INGREDIENTS is empty'
    else:
        list_ingredients = list()
        for ingredient in Ingredient.query.all():
            list_ingredients.append(ingredient.to_json())
        return list_ingredients


"""                  RECIPES                    """

user_recipes_bp = Blueprint("users_recipes", __name__, url_prefix="/user/recipes")

# http://127.0.0.1:5000/user/recipes/getall
@user_recipes_bp.route('/getall', methods=['GET'])
def getall_recipes():
    if RecipeRepository.data_recipe_is_empty():
        return 'The table Recipes is empty'
    else:
        list_recipes = list()
        for recipe in Recipe.query.all():
            list_recipes.append(recipe.to_json())
        return list_recipes

# http://127.0.0.1:5000/user/recipes/find_by_id?recipeid=
@user_recipes_bp.route('/find_by_id', methods=['GET' , 'POST'])
def find_recipe_by_id():
    recipe_id = request.args.get('recipeid')
    if not RecipeRepository.recipe_id_existe_in_data(recipe_id=recipe_id):
        return "Recipe does not existe in data"
    else:
        return RecipeRepository.get_recipe_by_id(recipe_id=recipe_id).to_json()

# http://127.0.0.1:5000/user/recipes/find_by_name?namerecipe=
@user_recipes_bp.route('/find_by_name', methods=['GET' , 'POST'])
def recipe_find_by_name():
    recipe_name = request.args.get('namerecipe')
    if not RecipeRepository.recipe_name_existe_in_data(recipe_name=recipe_name):
        return 'The recipe does not existe'
    else:
        recipe = RecipeRepository.get_recipe_by_name(recipe_name=recipe_name)
        return recipe.to_json()

# http://127.0.0.1:5000/user/recipes/find_by_ingredient?idingredient=
@user_recipes_bp.route('/find_by_ingredient', methods=['GET' , 'POST'])
def recipe_find_by_ingredient():
    """ "pour une liste d'ingredient_id donner return une list de toutes les recettes qui contient la list des id """
    ingridents_id = request.args.getlist('idingredient')
    if not ingridents_id:
        return "Aucun argument donner"
    else:
        return RecipeRepository.list_to_json(
            RecipeRepository.get_recipes_by_list_ingredients_id(list_ingrdients_id=ingridents_id)
        )

# http://127.0.0.1:5000/user/recipes/with_aout_ingredient?idingredient=
@user_recipes_bp.route('/with_aout_ingredient', methods=['GET' , 'POST'])
def recipe_find_without_ingredient():
    """ "pour une liste d'ingredient_id donner return une list de toutes les recettes qui ne contient pas la list des id """
    ingridents_id = request.args.getlist('idingredient')
    if not ingridents_id:
        return "Aucun argument donner"
    else:
        return RecipeRepository.list_to_json(
            RecipeRepository.get_recipes_without_list_ingredients_id(list_ingrdients_id=ingridents_id)
        )

# http://127.0.0.1:5000/user/recipes/like?recipeid= &userid=
@user_recipes_bp.route('/like', methods=['GET' , 'POST'])
def like_recipe():
    recipe_id = request.args.get('recipeid')
    user_id = request.args.get('userid')
    recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
    user = User.query.filter(User.id == user_id).first()
    if not (recipe or user):
        return f'The recipe or The user is not existe!!! {user} you can not check thes request {recipe}'
    elif FavoriteRecipe.query.filter(FavoriteRecipe.user_id == user_id, FavoriteRecipe.recipe_id==recipe_id).first():
        return f"the user {user.to_json()} has already liked this recipe {recipe.to_json()}"
    else:
        favorite_recipe = FavoriteRecipe(user_id=user_id, recipe_id=recipe_id)
        db.session.add(favorite_recipe)
        db.session.commit()
        return f"the user {user.to_json()} like instanttally this recipe {recipe.to_json()}"

# http://127.0.0.1:5000/user/recipes/dislike?recipeid= &userid=
@user_recipes_bp.route('/dislike', methods=['GET' , 'POST'])
def dislike_recipe():
    recipe_id = request.args.get('recipeid')
    user_id = request.args.get('userid')
    recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
    user = User.query.filter(User.id == user_id).first()
    if not (recipe or user):
        return f'The recipe or The user is not existe!!! {user} you can not check thes request {recipe}'
    else:
        if not FavoriteRecipe.query.filter(FavoriteRecipe.user_id == user_id, FavoriteRecipe.recipe_id==recipe_id).first():
            return f"the recipe {recipe.to_json()} is not in user's {user.to_json()} fvorite list  "
        else:
            favorite_recipe = FavoriteRecipe.query.filter(FavoriteRecipe.user_id == user_id, FavoriteRecipe.recipe_id==recipe_id).first()
            db.session.delete(favorite_recipe)
            db.session.commit()
            return f"the user {user.to_json()} dislike instanttally this recipe {recipe.to_json()}"

# http://127.0.0.1:5000/user/recipes/list_like
@user_recipes_bp.route('/list_like', methods=['GET' , 'POST'])
def get_list_like():
    user_id = request.args.get('userid')
    if not FavoriteRecipe.query.filter(FavoriteRecipe.user_id == user_id).all():
        return f'The user {user_id} has any recipe in his favorites list'
    else:
        list_favorite = list()
        for favorite_recipe in FavoriteRecipe.query.filter(FavoriteRecipe.user_id == user_id).all():
            recipe = Recipe.query.filter(Recipe.id == favorite_recipe.recipe_id).first()
            list_favorite.append(recipe.to_json())
        return list_favorite

