from db import db
from models import ingredient_table_name, recipe_ingredients_table_name


class Ingredient(db.Model):

    __tablename__ = ingredient_table_name

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(60), unique = True, nullable = False)

    """ Backpopulates, indicate which column to link when joinng 2 tables"""

    recipes = db.relationship('Recipe', secondary=recipe_ingredients_table_name, back_populates='ingredients')

    def __init__(self, name):
        self.name = name

