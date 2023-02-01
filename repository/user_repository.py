from db import db
from models.favoriterecipe import FavoriteRecipe
from models.user import User

class UserRepository():

    @classmethod
    def data_user_is_empty(cls):
        """ return True if and only if  data user is empty or NONE """
        data_list = User.query.all()
        return ((data_list is None) or (not data_list))

    @classmethod
    def user_id_existe_in_data(cls, user_id):
        """ return True if and only if l ID de l user existe dans la base de donnée """
        user = User.query.filter(
            User.id == user_id).first()
        return not user == None

    @classmethod
    def user_email_existe_in_data(cls, user_email):
        """ return True if and only if le email existe dans la base de donnée """
        user = User.query.filter(
            User.email == user_email).first()
        return not user == None

    @classmethod
    def user_password_existe_in_data(cls, user_password):
        """ return True if and only if le password existe dans la base de donnée """
        user = User.query.filter(
            User.password == user_password).first()
        return not user == None

    @classmethod
    def user_existe_in_data(cls, user):
        """ return True if and only if l'utilisateur existe dans la base de donnée """
        return UserRepository.user_name_existe_in_data(user_name=user.username)

    """ get USER by_id or by_name or getall"""
    @classmethod
    def get_user_by_id(cls, user_id):
        user = User.query.filter(
            User.id == user_id).first()
        return user

    @classmethod
    def get_user_by_name(cls, user_name):
        user = User.query.filter(
            User.username == user_name).first()
        return user


    """ Create User """
    @classmethod
    def create_user(cls, user_name, email, password, role_id ):
        new_user = User(username=user_name,email=email,password=password,role_id=role_id)
        db.session.add(new_user)
        db.session.commit()

    """ Delete User by_name or by_id"""

    @classmethod
    def delete_user_by_id(cls, user_id):
        user = UserRepository.get_user_by_id(user_id=user_id)
        favoriterecipes = FavoriteRecipe.query.filter(
            FavoriteRecipe.user_id == user_id).all()
        for favoriterecipe in favoriterecipes:
            db.session.delete(favoriterecipe)
            db.session.commit()
        db.session.delete(user)
        db.session.commit()

    """ Update User name or email or role or password """
    @classmethod
    def update_user_name(cls, user_id, new_name):
        user = UserRepository.get_user_by_id(user_id=user_id)
        user.username = new_name
        db.session.commit()

    @classmethod
    def update_user_email(cls, user_id, new_email):
        user = UserRepository.get_user_by_id(user_id=user_id)
        user.email = new_email
        db.session.commit()

    @classmethod
    def update_user_password(cls, user_id, new_password):
        user = UserRepository.get_user_by_id(user_id=user_id)
        user.password = new_password
        db.session.commit()

    @classmethod
    def update_user_role(cls, user_id, new_id_role):
        user = UserRepository.get_user_by_id(user_id=user_id)
        user.role_id = new_id_role
        db.session.commit()



