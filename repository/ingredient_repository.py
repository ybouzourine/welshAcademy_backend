from db import db
from models.ingredient import Ingredient
from models.recipeingredient import RecipeIngredient


class IngredientRepository():
    @classmethod
    def data_ingredient_is_empty(cls):
        """ return True if and only if  data ingredient is empty or NONE """
        data_list = Ingredient.query.all()
        return ((data_list is None) or (not data_list))

    @classmethod
    def ingredient_id_existe_in_data(cls, ingridient_id):
        """ return True if and only if l ID de l ingredient existe dans la base de donnée """
        ingredient = Ingredient.query.filter(
            Ingredient.id == ingridient_id).first()
        return not ingredient == None

    @classmethod
    def ingredient_name_existe_in_data(cls, ingridient_name):
        """ return True if and only if le name de l'ingredient existe dans la base de donnée """
        ingredient = Ingredient.query.filter(
            Ingredient.name == ingridient_name).first()
        return not ingredient == None

    @classmethod
    def ingredient_existe_in_data(cls, ingridient):
        """ return True if and only if l'ingredient existe dans la base de donnée """
        return IngredientRepository.ingredient_name_existe_in_data(ingridient.name)

    """ get INGREDIENT by_id or by_name or getall"""
    @classmethod
    def get_ingredient_by_id(cls, ingredient_id):
        ingredient = Ingredient.query.filter(
            Ingredient.id == ingredient_id).first()
        return ingredient

    @classmethod
    def get_ingredient_by_name(cls, ingredient_name):
        ingredient = Ingredient.query.filter(
            Ingredient.name == ingredient_name).first()
        return ingredient


    """ Create INGREDIENT with_name """
    @classmethod
    def create_ingredient(cls, ingredient_name):
        new_ingredient = Ingredient(name=ingredient_name)
        db.session.add(new_ingredient)
        db.session.commit()

    """ Delete INGREDIENT ingredient or by_name or by_id"""
    @classmethod
    def delete_ingredient_by_id(cls,ingredient_id):
        ingredient = IngredientRepository.get_ingredient_by_id(ingredient_id=ingredient_id)
        recipeingredients = RecipeIngredient.query.filter(
            RecipeIngredient.ingredient_id == ingredient_id).all()
        for recipeingredient in recipeingredients:
            db.session.delete(recipeingredient)
            db.session.commit()
        db.session.delete(ingredient)
        db.session.commit()


    """ Update INGREDIENT name """
    @classmethod
    def update_name_ingredient(cls, ingredient_id, new_name):
        ingredient = IngredientRepository.get_ingredient_by_id(ingredient_id)
        ingredient.name = new_name
        db.session.commit()




