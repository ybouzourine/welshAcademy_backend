from db import db
from models import recipe_table_name, recipe_ingredients_table_name, user_table_name, favorite_recipe_table_name


class Recipe(db.Model):

    __tablename__ = recipe_table_name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(60))

    ingredients = db.relationship('Ingredient', secondary=recipe_ingredients_table_name, back_populates="recipes")

    users = db.relationship('User', secondary=favorite_recipe_table_name, back_populates="recipes")


    def __init__(self, name, description):
        self.name = name
        self.description = description

    def to_json(self):
        return {
            'name': self.name,
            'description': self.description
        }