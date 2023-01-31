from flask import Blueprint, jsonify, request, Response

from db import db
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.recipeingredient import RecipeIngredient
from models.user import User, Role


"""                      INGREDIENTS                          """
admin_ingredient_bp = Blueprint("admin_ingredient", __name__, url_prefix="/admin/ingredients")

#http://127.0.0.1:5000/admin/ingredients/create?ingredientname=tomate
@admin_ingredient_bp.route('/create', methods=['GET' , 'POST'])
def create_ingredient():
    ingredient_name= request.args.get('ingredientname')
    if not Ingredient.query.filter(Ingredient.name == ingredient_name).first():
        new_ingredient = Ingredient(name=ingredient_name)
        db.session.add(new_ingredient)
        db.session.commit()
        return "Ingredient created "
    else:
        return "Ingredient exists already"

#http://127.0.0.1:5000/admin/ingredients/delete?id=
@admin_ingredient_bp.route('/delete', methods=['GET', 'POST'])
def delete_ingredient():
    ingredient_id = request.args.get('id')
    #ingredient = get_ingredient_by_id(ingredient_id)
    ingredient = Ingredient.query.filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
      return 'Can\'t delete ingredient. The ingredient does not exist'
    else:
        #delete_ingredient(ingredient)
        db.session.delete(ingredient)
        db.session.commit()
        return 'Ingredient deleted successfully'

#http://127.0.0.1:5000/admin/ingredients/update?id=
@admin_ingredient_bp.route('/update', methods=['GET' , 'POST'])
def update_ingredient():
    ingredient_id = request.args.get('id')
    ingredient_new_name = request.args.get('newname')

    ingredient = Ingredient.query.filter(Ingredient.id == ingredient_id).first()
    #ingredient = get_ingredient_by_id(ingredient_id)
    if not ingredient:
        return 'The ingredient doest not exist'
    else:
        #update_ingredient(ingredient_id,new_ingredient_name)
        if ingredient.name != ingredient_new_name:
            ingredient.name = ingredient_new_name
            db.session.commit()
        return 'Ingredient updated successfully'

# http://127.0.0.1:5000/admin/ingredients/getall
@admin_ingredient_bp.route('/getall', methods=['GET' , 'POST'])
def getall_ingredients():
    if not Ingredient.query.all():
        return 'The table INGREDIENTS is empty'
    else:
        list_ingredients = list()
        for ingredient in Ingredient.query.all():
            list_ingredients.append(ingredient.to_json())
        return list_ingredients



"""                         USERS                                   """
admin_user_bp = Blueprint("admin_user", __name__, url_prefix="/admin/users")

#http://127.0.0.1:5000/admin/users/create?username=youcef&email=youcefdaicine&password=lesgroupe&roleid=2
@admin_user_bp.route('/create', methods=['GET' , 'POST'])
def create_user():
    username= request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    role_id = request.args.get('roleid')

    if not User.query.filter(User.username == username).first():
        new_user = User(username=username, email=email, password=password, role_id=role_id)
        db.session.add(new_user)
        db.session.commit()
        return "User created "
    else:
        return "User exists already"

# http://127.0.0.1:5000/admin/users/delete?id=3
@admin_user_bp.route('/delete', methods=['GET'])
def delete_user():
    user_id = request.args.get('id')
    if not User.query.filter(User.id == user_id).first():
        return 'The User doest not exist'
    else:
        user = User.query.filter(User.id == user_id).first()
        db.session.delete(user)
        db.session.commit()
        return 'User deleted successfully'

# http://127.0.0.1:5000/admin/users/update?name=
@admin_user_bp.route('/update/name', methods=['GET' , 'POST'])
def update_username():
    user_id = request.args.get('id')
    user_new_name = request.args.get('newname')

    if not User.query.filter(User.id == user_id).first():
        return 'The User doest not exist'
    else:
        user = User.query.filter(User.id == user_id).first()
        if user.username != user_new_name:
            user.username = user_new_name
            db.session.commit()
        return 'User updated_name successfully'

# http://127.0.0.1:5000/admin/users/update?email=
@admin_user_bp.route('/update/email', methods=['GET' , 'POST'])
def update_email():
    user_id = request.args.get('id')
    user_new_email = request.args.get('newemail')

    if not User.query.filter(User.id == user_id).first():
        return 'The User doest not exist'
    else:
        user = User.query.filter(User.id == user_id).first()
        if user.email != user_new_email:
            user.email = user_new_email
            db.session.commit()
        return 'User updated_email successfully'

# http://127.0.0.1:5000/admin/users/update?password=
@admin_user_bp.route('/update/password', methods=['GET' , 'POST'])
def update_password():
    user_id = request.args.get('id')
    new_password = request.args.get('newpassword')

    if not User.query.filter(User.id == user_id).first():
        return 'The User doest not exist'
    else:
        user = User.query.filter(User.id == user_id).first()
        if user.password != new_password:
            user.password = new_password
            db.session.commit()
        return 'User updated_password successfully'

# http://127.0.0.1:5000/admin/users/getall
@admin_user_bp.route('/getall', methods=['GET' , 'POST'])
def getall_users():
    if not User.query.all():
        return 'The table USERS is empty'
    else:
        list_users = list()
        for user in User.query.all():
            list_users.append(user.to_json())
        return list_users

"""                         RECIPES                   """
admin_recipe_bp = Blueprint("admin_recipe", __name__, url_prefix="/admin/recipes")

#http://127.0.0.1:5000/admin/recipes/create_with_quantitis?recipename=omelette&recipedescription=melangeomeletteavecfromage&ingredients=1&ingredients=2&ingredients=3&quantity=gr&quantity=br&quantity=fr
@admin_recipe_bp.route('/create_with_quantitis', methods=['GET' , 'POST'])
def create_recipe():
    recipe_name= request.args.get('recipename')
    recipe_description=request.args.get('recipedescription')
    recipe_ingredients_id=request.args.getlist('ingredients')
    quantities=request.args.getlist('quantity')

    if not Recipe.query.filter(Recipe.name == recipe_name).first():
        new_recipe = Recipe(name=recipe_name, description=recipe_description)
        db.session.add(new_recipe)
        db.session.commit()
        if Recipe.query.filter(Recipe.name == recipe_name).first():
            recipe_id=new_recipe.id
            for i in range(len(recipe_ingredients_id)):
                recipeingredients = RecipeIngredient(quantity=quantities[i],recipe_id=recipe_id, ingredient_id=recipe_ingredients_id[i])
                db.session.add(recipeingredients)
                db.session.commit()
            return 'recipe created'
    else:
        return 'recipe exists already '


# http://127.0.0.1:5000/admin/recipes/delete?id=3
@admin_recipe_bp.route('/delete', methods=['GET'])
def delete_recipe():
    recipe_id = request.args.get('id')
    if not Recipe.query.filter(Recipe.id == recipe_id).first():
        return 'The Recipe doest not exist'
    else:
        recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
        db.session.delete(recipe)
        db.session.commit()
        return 'Recipe delete successfully'

# http://127.0.0.1:5000/admin/recipes/update/name?id=2&newnamerecipe=
@admin_recipe_bp.route('/update/name', methods=['GET' , 'POST'])
def update_name_recipe():
    recipe_id = request.args.get('id')
    new_name_recipe = request.args.get('newnamerecipe')
    if not Recipe.query.filter(Recipe.id == recipe_id).first():
        return 'The Recipe doest not exist'
    else:
        recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
        if recipe.name != new_name_recipe:
            recipe.name = new_name_recipe
            db.session.commit()
        return 'Recipe updated_name successfully'

# http://127.0.0.1:5000/admin/recipes/update/description?id=2&newdescriptionrecipe=
@admin_recipe_bp.route('/update/description', methods=['GET' , 'POST'])
def update_description_recipe():
    recipe_id = request.args.get('id')
    new_description_recipe = request.args.get('newdescriptionrecipe')
    if not Recipe.query.filter(Recipe.id == recipe_id).first():
        return 'The Recipe doest not exist'
    else:
        recipe = Recipe.query.filter(Recipe.id == recipe_id).first()
        if recipe.description != new_description_recipe:
            recipe.description = new_description_recipe
            db.session.commit()
        return 'Recipe updated_description successfully'

# http://127.0.0.1:5000/admin/recipes/getall
@admin_recipe_bp.route('/getall', methods=['GET' , 'POST'])
def getall_recipes():
    if not Recipe.query.all():
        return 'The table Recipes is empty'
    else:
        list_recipes = list()
        for recipe in Recipe.query.all():
            list_recipes.append(recipe.to_json())
        return list_recipes

"""                        Roles                               """
admin_role_bp = Blueprint("admin_role", __name__, url_prefix="/admin/roles")

# http://127.0.0.1:5000/admin/roles/create?rolename=user

@admin_role_bp.route('/create', methods=['GET' , 'POST'])
def create_role():
    role_name = request.args.get('rolename')
    if not Role.query.filter(Role.role_name == role_name).first():
        new_role = Role(role_name=role_name)
        db.session.add(new_role)
        db.session.commit()
        return "New role created "
    else:
        return "Role exists already"

# http://127.0.0.1:5000/admin/roles/getall
@admin_role_bp.route('/getall', methods=['GET' , 'POST'])
def getall_roles():
    if not Role.query.all():
        return 'The table Roles is empty'
    else:
        list_roles = list()
        for role in Role.query.all():
            list_roles.append(role.to_json())
        return list_roles
