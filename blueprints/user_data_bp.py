from flask import Blueprint, request, redirect, flash, render_template, current_app
import os
import base64
import json

ALLOWED_EXTENSIONS = {"webp", "png", "jpg", "jpeg", "gif"}

__name__ = Blueprint("users", __name__, url_prefix="/users")


def check_file_existence(path):
    try:
        file_size = os.path.getsize(path)
        if file_size == 0:
            print("File is empty")
            return False
        else:
            print("File is NOT empty")
            return True
    except FileNotFoundError as e:
        print(f"File NOT found: {e}")
        return False


def endcode_base_64(file):
    """converte arquivo para base64"""
    try:
        base64_encoded = base64.b64encode(file)
        return base64_encoded.decode("utf-8")
    except:
        flash("Error on converting file")


def write_user_data(json_data):
    """escreve registro no arquivo no db.json"""
    file_path = f"{current_app.config['DB_FOLDER']}/db.json"
    try:
        if not check_file_existence(file_path):
            # inicializa arquivo caso vazio ou inexistente
            with open(file_path, "w", encoding="utf-8") as file_db:
                file_db.write(json.dumps({"user_data": []}))

        # carrega arquivo json como dict, adiciona o novo item, converte pra json dnv e escreve no arquivo
        with open(file_path, "r+", encoding="utf-8") as file_db:
            file_content = json.load(file_db)
            file_content["user_data"].append(json_data)
            file_db.seek(0)
            print(file_db.seek(0))
            json.dump(
                file_content, file_db, ensure_ascii=False, sort_keys=True, indent=4
            )
    except:
        flash("Error on saving data")


def save_user_data(request):
    error = None
    success = None
    user_data = {"name": None, "age": None, "photo": None}

    if "photo" not in request.files:
        flash("sem arquivo")
        redirect(request.url)
    elif request.files["photo"] == "":
        flash("Nenhum arquivo selecionado")
        return redirect(request.url)
    else:
        try:
            user_data["name"] = request.form["name"]
            user_data["age"] = request.form["age"]
            user_data["photo"] = endcode_base_64(request.files["photo"].read())

            write_user_data(user_data)

            success = "DADOSSSS!!! 😋😋😋"
        except Exception as e:
            print(e)
            error = "Falha em pegar teus dados :((("
        finally:
            return render_template("main.html", error=error, success=success)


@__name__.route("/", methods=["GET", "POST"])
def handle_form():
    if request.method == "GET":
        return render_template("main.html")
    if request.method == "POST":
        return save_user_data(request)
