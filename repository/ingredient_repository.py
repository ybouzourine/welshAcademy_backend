# from db import db
# from models.ingredient import Ingredient
#
# class IngredientRepository():
#     def get_ingredient_by_id(ingredient_id):
#         ingredient = Ingredient.query.filter(
#             Ingredient.id == ingredient_id).first()
#         return ingredient
#
#
#     def get_ingredient_by_name(ingredient_name):
#         ingredient = Ingredient.query.filter(
#             Ingredient.name == ingredient_name).first()
#         return ingredient
#
#
#     def create_ingredient(ingredient_name):
#         new_ingredient = Ingredient(name=ingredient_name)
#         db.session.add(new_ingredient)
#         db.session.commit()
#
#
#     def delete_ingredient(ingredient):
#         db.session.delete(ingredient)
#         db.session.commit()
#
#     def update_ingredient(ingredient_id, ingredient_new_name):
#         ingredient = get_ingredient_by_id(ingredient_id)
#         if ingredient.name != ingredient_new_name:
#             ingredient.name = ingredient_new_name
#             db.session.commit()
