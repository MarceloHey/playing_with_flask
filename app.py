from flask import Flask
from blueprints import user_data_bp

DB_FOLDER = "db"

app = Flask(__name__)
app.config["DB_FOLDER"] = DB_FOLDER
app.secret_key = "supersecretkey"

app.register_blueprint(user_data_bp.__name__)
