from db import db
from models import user_table_name, role_table_name, recipe_ingredients_table_name,favorite_recipe_table_name
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin


class User(db.Model, UserMixin):

    __tablename__ = user_table_name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable = False)
    email = db.Column(db.String(60), unique=True, nullable = False)
    password = db.Column(db.String(60), unique=True)
    role = db.relationship('Role', backref='user')

    recipes = db.relationship('Recipe', secondary=favorite_recipe_table_name, back_populates='users')


    def __init__(self, name, email, password):
        self.username = name
        self.email = email
        self.password = password

    def to_json(self):
        return {
            'name': self.name,
            'first_name': self.first_name,
            'email': self.email,
            'password': self.password
        }

class Role(db.Model):
    __tablename__ = role_table_name

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(60), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, role):
        self.role_name = role
