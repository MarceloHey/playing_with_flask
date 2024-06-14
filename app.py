from flask import Flask

DB_FOLDER = "db"

app = Flask(__name__)
app.config["DB_FOLDER"] = DB_FOLDER
app.secret_key = "supersecretkey"

from blueprints import user_data

app.register_blueprint(user_data.__name__)
