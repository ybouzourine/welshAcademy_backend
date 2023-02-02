from db import db
from models.favoriterecipe import FavoriteRecipe
from models.recipe import Recipe
from models.recipeingredient import RecipeIngredient
from repository.ingredient_repository import IngredientRepository


class RecipeRepository():

    @classmethod
    def data_recipe_is_empty(cls):
        """ return True if and only if the data recipe is empty or NONE """
        data_list = Recipe.query.all()
        return ((data_list is None) or (not data_list))

    @classmethod
    def recipe_id_existe_in_data(cls, recipe_id):
        """ return True if and only if the recipe ID exists in the database """
        recipe = Recipe.query.filter(
            Recipe.id == recipe_id).first()
        return not recipe == None

    @classmethod
    def recipe_name_existe_in_data(cls, recipe_name):
        """ return True if and only if the recipe name exists in the database """
        recipe = Recipe.query.filter(
            Recipe.name == recipe_name).first()
        return not recipe == None
    @classmethod
    def recipe_existe_in_data(cls, recipe):
        """ return True if and only if the recipe exists in the database """
        return RecipeRepository.recipe_name_existe_in_data(recipe_name=recipe.name)

    """ get RECIPE by_id, by_name """
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
            recipeingredients = RecipeIngredient(recipe_id=recipe_id, ingredient_id=list_ingredient_id[int(i)],
                                                 quantity=list_ingredient_quantity[int(i)])
            db.session.add(recipeingredients)
            db.session.commit()

    """ Delete recipe or by_id"""
    @classmethod
    def delete_recipe_by_id(cls, recipe_id):
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

    """ Update Recipe name or description  """
    @classmethod
    def update_recipe_name(cls, recipe_id, new_name):
        recipe = RecipeRepository.get_recipe_by_id(recipe_id=recipe_id)
        recipe.name = new_name
        db.session.commit()

    @classmethod
    def update_recipe_decsription(cls, recipe_id, new_description):
        recipe = RecipeRepository.get_recipe_by_id(recipe_id=recipe_id)
        recipe.description = new_description
        db.session.commit()


    @classmethod
    def get_recipes_by_ingredient_id(cls, ingrdient_id):
        """ Returns a list of recipes such that each recipe contains the ingredient given in parameter
            else return an empty set """
        if not IngredientRepository.ingredient_id_existe_in_data(ingridient_id=ingrdient_id):
            return list()
        else:
            recipeingredients = RecipeIngredient.query.filter(
                    RecipeIngredient.ingredient_id == ingrdient_id
                ).all()
            if not recipeingredients:
                return list()
            else:
                list_recipes = list()
                for recipe_ingredient in recipeingredients:
                    recipe = RecipeRepository.get_recipe_by_id(recipe_id=recipe_ingredient.recipe_id)
                    list_recipes.append(recipe)
            return list_recipes

    @classmethod
    def get_recipes_by_list_ingredients_id(cls, list_ingrdients_id):
        """ get a list of recipes such that each recipe contains all
            the list of ingredients given in parameter """
        list_recipes = set(Recipe.query.all())
        for id in list_ingrdients_id:
            list_recipes = list_recipes.intersection(set(RecipeRepository.get_recipes_by_ingredient_id(ingrdient_id=id)))
        return list_recipes

    @classmethod
    def get_recipes_without_list_ingredients_id(cls, list_ingrdients_id):
        """ get a list of recipes such that each recipe does not contain
            any ingredient given in the list of parameters """
        return set(Recipe.query.all()).difference(
            RecipeRepository.get_recipes_by_list_ingredients_id(list_ingrdients_id)
        )

    @classmethod
    def list_to_json(cls, list_recipes):
        list_to_json = list()
        for recipe in list_recipes:
            list_to_json.append(recipe.to_json())
        return list_to_json.__str__()




