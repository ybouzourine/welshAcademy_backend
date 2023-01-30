from sqlalchemy.orm import backref

from db import db
from models import recipe_ingredients_table_name
from models.ingredient import Ingredient
from models.recipe import Recipe


class RecipeIngredient(db.Model):

    __tablename__ = recipe_ingredients_table_name
    id = db.Column(db.Integer,primary_key = True)

    recipe_id = db.Column(db.Integer,db.ForeignKey('recipe.id'))
    ingredient_id = db.Column(db.Integer,db.ForeignKey('ingredient.id'))
    quantity = db.Column(db.String(60), nullable=False)

    def __init__(self, quantity, recipe_id,ingredient_id):
        self.quantity = quantity
        self.recipe_id= recipe_id
        self.ingredient_id=ingredient_id


