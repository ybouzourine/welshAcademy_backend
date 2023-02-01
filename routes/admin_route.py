from flask import Blueprint, jsonify, request, Response

from db import db
from models.ingredient import Ingredient
from models.recipe import Recipe
from models.recipeingredient import RecipeIngredient
from models.user import User, Role
from repository.ingredient_repository import IngredientRepository
from repository.recipe_repository import RecipeRepository
from repository.user_repository import UserRepository


"""                      INGREDIENTS                          """

admin_ingredient_bp = Blueprint("admin_ingredient", __name__, url_prefix="/admin/ingredients")

#http://127.0.0.1:5000/admin/ingredients/create?ingredientname=tomate
@admin_ingredient_bp.route('/create', methods=['GET' , 'POST'])
def create_ingredient():
    ingredient_name = request.args.get('ingredientname')
    if IngredientRepository.ingredient_name_existe_in_data(ingridient_name=ingredient_name):
        return "Ingredient exists already"
    else:
        IngredientRepository.create_ingredient(ingredient_name=ingredient_name)
        return "Ingredient created "

#http://127.0.0.1:5000/admin/ingredients/delete?id=
@admin_ingredient_bp.route('/delete', methods=['GET', 'POST'])
def delete_ingredient():
    ingredient_id = request.args.get('id')
    if (ingredient_id is not None):
        if not IngredientRepository.ingredient_id_existe_in_data(ingridient_id=ingredient_id):
            return "Can\'t delete ingredient. The ingredient does not exist"
        else:
            IngredientRepository.delete_ingredient_by_id(ingredient_id=ingredient_id)
            return "Ingredient deleted successfully"
    else:
        return "Can\'t delete ingredient.just give ingredint_id "

#http://127.0.0.1:5000/admin/ingredients/update?id=&newname=
@admin_ingredient_bp.route('/update', methods=['GET' , 'POST'])
def update_ingredient():
    ingredient_id = request.args.get('id')
    new_name = request.args.get('newname')
    if not IngredientRepository.ingredient_id_existe_in_data(ingridient_id=ingredient_id):
        return 'Can not updat Ingredient, The ingredient doest not exist'
    else:
        if IngredientRepository.ingredient_name_existe_in_data(ingridient_name=new_name):
            return 'Can not updat Ingredient, The ingredient existe already'
        else:
            IngredientRepository.update_name_ingredient(ingredient_id=ingredient_id,new_name=new_name)
            return 'Ingredient updated successfully'

# http://127.0.0.1:5000/admin/ingredients/getall
@admin_ingredient_bp.route('/getall', methods=['GET' , 'POST'])
def getall_ingredients():
    if IngredientRepository.data_ingredient_is_empty():
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
    user_name= request.args.get('username')
    email = request.args.get('email')
    password = request.args.get('password')
    role_id = request.args.get('roleid')

    if UserRepository.user_email_existe_in_data(user_email=email) \
            or UserRepository.user_password_existe_in_data(user_password=password):
        return "password or email exists already"
    else:
        if (int(role_id) == 2):
            UserRepository.create_user(
                user_name=user_name,
                email=email,
                password=password,
                role_id=role_id
            )
            return "User created"
        else:
            return "User not created, Role_id of user us equals 2"

# http://127.0.0.1:5000/admin/users/delete?id=3
@admin_user_bp.route('/delete', methods=['GET'])
def delete_user():
    user_id = request.args.get('id')
    if not UserRepository.user_id_existe_in_data(user_id=user_id):
        return 'The User doest not exist'
    else:
        UserRepository.delete_user_by_id(user_id=user_id)
        return 'User deleted successfully'

# http://127.0.0.1:5000/admin/users/update?id=&newname=&newemail=&newpassword=&newroleid=
@admin_user_bp.route('/update', methods=['GET' , 'POST'])
def update_username():
    user_id = request.args.get('id')
    user_new_name = request.args.get('newname')
    user_new_email = request.args.get('newemail')
    user_new_password = request.args.get('newpassword')
    user_new_role_id = request.args.get('newroleid')

    if not UserRepository.user_id_existe_in_data(user_id=user_id):
        return 'The User doest not exist'
    else:
        user = UserRepository.get_user_by_id(user_id=user_id)
        messege = "Update: "
        if not ((user_new_name is None) or (user_new_name == "") or (user.username == user_new_name)):
            UserRepository.update_user_name(user_id=user_id, new_name=user_new_name)
            messege += "/username_updated / "
        if not ((user_new_email is None) or (user_new_email == "") or (user.email == user_new_email)):
            UserRepository.update_user_email(user_id=user_id, new_email=user_new_email)
            messege += "/email_updated / "
        if not ((user_new_password is None) or (user_new_password == "") or (user.password == user_new_password)):
            UserRepository.update_user_password(user_id=user_id, new_password=user_new_password)
            messege += "/password_updated / "
        if not ((user_new_role_id is None) or (user_new_role_id == "") or (user.role_id == int(user_new_role_id))):
            UserRepository.update_user_role(user_id=user_id, new_id_role=user_new_role_id)
            messege += "/role_id_updated / "

        if messege == "Update: ":
            return "No Update, soit vous aver donner exactement les meme info ou aucune information"
        else:
            return messege

# http://127.0.0.1:5000/admin/users/getall
@admin_user_bp.route('/getall', methods=['GET' , 'POST'])
def getall_users():
    if UserRepository.data_user_is_empty():
        return 'The table USERS is empty'
    else:
        list_users = list()
        for user in User.query.all():
            list_users.append(user.to_json())
        return list_users


"""                         RECIPES                   """

admin_recipe_bp = Blueprint("admin_recipe", __name__, url_prefix="/admin/recipes")

#http://127.0.0.1:5000/admin/recipes/create?recipename=&recipedescription=&ingredients=1&ingredients=2&ingredients=3&quantity=gr&quantity=br&quantity=fr
@admin_recipe_bp.route('/create', methods=['GET' , 'POST'])
def create_recipe():
    recipe_name= request.args.get('recipename')
    recipe_description=request.args.get('recipedescription')
    recipe_ingredients_id=request.args.getlist('ingredients')
    quantities=request.args.getlist('quantity')
    if RecipeRepository.recipe_name_existe_in_data(recipe_name=recipe_name):
        return 'recipe exists already '
    else:
        if  (0 < len(recipe_ingredients_id) == len(quantities)):
            if recipe_ingredients_id != list(set(recipe_ingredients_id)):
                return "La recette ne peut pas contenir des ingredient doubler"
            else:
                RecipeRepository.create_recipe(
                    recipe_name=recipe_name,
                    description=recipe_description,
                    list_ingredient_id=recipe_ingredients_id,
                    list_ingredient_quantity=quantities
                )
            return 'recipe created'
        else:
            return "on peut pas creer une recette avec 0 ingredient ou avec une liste d'ingredients sans quantite"

# http://127.0.0.1:5000/admin/recipes/delete?id=3
@admin_recipe_bp.route('/delete', methods=['GET'])
def delete_recipe():
    recipe_id = request.args.get('id')
    if not RecipeRepository.recipe_id_existe_in_data(recipe_id=recipe_id):
        return 'The Recipe doest not exist'
    else:
        RecipeRepository.delete_recipe_by_id(recipe_id=recipe_id)
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
