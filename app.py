from flask import Flask
from flask_login import LoginManager

from db import db
from models import ingredient, recipe, user, favoriterecipe, recipeingredient


from models.user import User, Role
from routes.admin_route import admin_ingredient_bp, admin_user_bp, admin_role_bp
from routes.user_route import user_bp
from routes.auth import auth_bp
from routes.recipe_route import recipe_bp
from routes.ingredients_route import ingredient_bp



def create_app():
    app = Flask(__name__)
    """Configuration de l'URI de connexion à la base de données"""
    app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:0000@localhost:5432/backendb0"
    app.config['SECRET_KEY'] = "secretkey"


    # login_manager = LoginManager()
    # login_manager.login_view = 'login'
    # login_manager.init_app(app)

    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(int(user_id))

    db.app = app
    db.init_app(app)

    app.register_blueprint(admin_user_bp)
    app.register_blueprint(admin_ingredient_bp)
    app.register_blueprint(admin_role_bp)

    app.register_blueprint(recipe_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ingredient_bp)


    # Il faut rajouter le context... à toi de chercher ce que ça veut dire
    with app.app_context():
        db.create_all()
        """           Creation de l'admin         """

        if not Role.query.filter(Role.role_name=="admin").first():
            role_admin = Role(role_name="admin")
            db.session.add(role_admin)
            db.session.commit()
        if Role.query.filter(Role.role_name=="admin").first():
            role = Role.query.filter(Role.role_name=="admin").first()
            if not User.query.filter(User.email == 'admin@admin.com').first():
                admin = User(username="admin", email='admin@admin.com',password='admin', role_id=role.id)
                #admin.append(Role.query.get(role.id))
                db.session.add(admin)
            db.session.commit()
        app.run(debug=True)
        


    return app