
from db import db
from models import favorite_recipe_table_name

from models.recipe import Recipe
from models.user import User


class FavoriteRecipe(db.Model):

    __tablename__ = favorite_recipe_table_name
    id = db.Column(db.Integer,primary_key = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE",onupdate="CASCADE"))
    recipe_id = db.Column(db.Integer,db.ForeignKey('recipe.id'))


    def __init__(self, user_id,recipe_id):
        self.user_id = user_id
        self.recipe_id= recipe_id

