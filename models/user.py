from db import db
from models import user_table_name, role_table_name, recipe_ingredients_table_name,favorite_recipe_table_name
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin


class User(db.Model, UserMixin):

    __tablename__ = user_table_name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable = False)
    email = db.Column(db.String(60), unique=True, nullable = False)
    password = db.Column(db.String(60), unique=True)

    #role = db.relationship('Role', backref='user')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    recipes = db.relationship('Recipe', secondary=favorite_recipe_table_name, back_populates='users')


    def __init__(self, username, email, password,role_id):
        self.username = username
        self.email = email
        self.password = password
        self.role_id=role_id

    def to_json(self):
        role = "user"
        if self.role_id == 1:
            role = "admin_routes"
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'role': role
        }

class Role(db.Model):
    __tablename__ = role_table_name

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(60), nullable=False)

    user_id = db.relationship('User', backref='role')
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, role_name):
        self.role_name = role_name

    def to_json(self):
        return {
            'id': self.id,
            'role': self.role_name,
        }