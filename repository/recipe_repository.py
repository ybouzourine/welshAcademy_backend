from db import db
from models.favoriterecipe import FavoriteRecipe
from models.recipe import Recipe
from models.recipeingredient import RecipeIngredient


class RecipeRepository():

    @classmethod
    def data_recipe_is_empty(cls):
        """ return True if and only if  data recipe is empty or NONE """
        data_list = Recipe.query.all()
        return ((data_list is None) or (not data_list))

    @classmethod
    def recipe_id_existe_in_data(cls, recipe_id):
        """ return True if and only if l ID of recipe existe dans la base de donnée """
        recipe = Recipe.query.filter(
            Recipe.id == recipe_id).first()
        return not recipe == None

    @classmethod
    def recipe_name_existe_in_data(cls, recipe_name):
        """ return True if and only if l name of recipe existe dans la base de donnée """
        recipe = Recipe.query.filter(
            Recipe.name == recipe_name).first()
        return not recipe == None
    @classmethod
    def recipe_existe_in_data(cls, recipe):
        """ return True if and only if l'recette existe dans la base de donnée """
        return RecipeRepository.recipe_name_existe_in_data(recipe_name=recipe.name)

    """ get RECIPE by_id or by_name """
    @classmethod
    def get_recipe_by_id(cls, recipe_id):
        recipe = Recipe.query.filter(
            Recipe.id == recipe_id).first()
        return recipe

    @classmethod
    def get_recipe_by_name(cls, recipe_name):
        recipe = Recipe.query.filter(
            Recipe.name == recipe_name).first()
        return recipe

    """ Create recipe """
    @classmethod
    def create_recipe(cls, recipe_name, description, list_ingredient_id, list_ingredient_quantity):
        new_recipe = Recipe(name=recipe_name, description=description)
        db.session.add(new_recipe)
        db.session.commit()
        recipe_id = RecipeRepository.get_recipe_by_name(recipe_name=recipe_name).id
        for i in range(len(list_ingredient_quantity)):
            recipeingredients = RecipeIngredient( recipe_id=recipe_id,ingredient_id=list_ingredient_id[int(i)],quantity=list_ingredient_quantity[int(i)])
            db.session.add(recipeingredients)
            db.session.commit()


    """ Delete recipe by_name or by_id"""
    @classmethod
    def delete_recipe_by_id(cls,recipe_id):
        recipe = RecipeRepository.get_recipe_by_id(recipe_id=recipe_id)
        recipeingredients = RecipeIngredient.query.filter(
            RecipeIngredient.recipe_id == recipe_id).all()
        for recipeingredient in recipeingredients:
            db.session.delete(recipeingredient)
            db.session.commit()
        favoriterecipes = FavoriteRecipe.query.filter(
            FavoriteRecipe.recipe_id == recipe_id).all()
        for favoriterecipe in favoriterecipes:
            db.session.delete(favoriterecipe)
            db.session.commit()
        db.session.delete(recipe)
        db.session.commit()

    """ Update Recipe name or email or role or password """
    @classmethod
    def update_recipe_name(cls, recipe_id, new_name):
        recipe = RecipeRepository.get_recipe_by_id(recipe_id=recipe_id)
        recipe.name = new_name
        db.session.commit()


