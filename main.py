from app import create_app
from db import db
from models.user import User, Role

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1")