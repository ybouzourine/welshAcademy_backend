import numpy as numpy
from flask import Blueprint, jsonify, request, Response

from db import db
from models.favoriterecipe import FavoriteRecipe
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.recipeingredient import RecipeIngredient
from models.user import User


"""                  INGREDIENTS                    """

user_ingredients_bp = Blueprint("users_ingredients", __name__, url_prefix="/user/ingredients")

# http://127.0.0.1:5000/user/ingredients/getall
@user_ingredients_bp.route('/getall', methods=['GET', 'POST'])
def getall_ingredients():
    if not Ingredient.query.all():
        return 'The table Ingredients is empty'
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
    if not Recipe.query.all():
        return 'The table Recipes is empty'
    else:
        list_recipes = list()
        for recipe in Recipe.query.all():
            list_recipes.append(recipe.to_json())
        return list_recipes

# http://127.0.0.1:5000/user/recipes/find_by_id?id=
@user_recipes_bp.route('/find_by_id', methods=['GET' , 'POST'])
def find_recipe_by_id():
    recipe_id = request.args.get('id')
    if not Recipe.query.filter(Recipe.id == recipe_id):
        return 'The recipe does not existe'
    else:
        recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
        return recipe.to_json()

# http://127.0.0.1:5000/user/recipes/find_by_name?namerecipe=
@user_recipes_bp.route('/find_by_name', methods=['GET' , 'POST'])
def recipe_find_by_name():
    name_recipe = request.args.get('namerecipe')
    if not Recipe.query.filter(Recipe.name == name_recipe):
        return 'The recipe does not existe'
    else:
        recipe = Recipe.query.filter(Recipe.name == name_recipe).first()
        return recipe.to_json()

# http://127.0.0.1:5000/user/recipes/find_by_ingredient?nameingredient=
@user_recipes_bp.route('/find_by_ingredient', methods=['GET' , 'POST'])
def recipe_find_by_ingredient():
    name_ingredient = request.args.get('nameingredient')
    ingredient_id = Ingredient.query.filter(Ingredient.name == name_ingredient).first().id
    recipes_containt_ingredient = RecipeIngredient.query.filter(RecipeIngredient.ingredient_id == ingredient_id).all()
    if not recipes_containt_ingredient:
        return 'aucune recette contient l ingredient'
    else:
        list_recipes = list()
        for recipe_containt_ingredient in recipes_containt_ingredient:
            recipe_id = recipe_containt_ingredient.recipe_id
            recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
            list_recipes.append(recipe.to_json())
    return list_recipes

# http://127.0.0.1:5000/user/recipes/with_aout_ingredient?nameingredient=
@user_recipes_bp.route('/with_aout_ingredient', methods=['GET' , 'POST'])
def recipe_find_without_ingredient():
    name_ingredient = request.args.get('nameingredient')
    ingredient_id = Ingredient.query.filter(Ingredient.name == name_ingredient).first().id
    recipes_no_ingredient = RecipeIngredient.query.filter(RecipeIngredient.ingredient_id != ingredient_id).all()
    if not recipes_no_ingredient:
        return f" all recipes contain the ingredient {name_ingredient}"
    else:
        list_recipes = list()
        for recipe_no_ingredient in recipes_no_ingredient:
            recipe_id = recipe_no_ingredient.recipe_id
            recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
            if recipe.to_json() not in list_recipes:
                list_recipes.append(recipe.to_json())
    return list_recipes


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

