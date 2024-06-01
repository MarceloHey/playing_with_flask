from flask import render_template
from flask import Flask, request, redirect, flash
import os
import base64
import json

DB_FOLDER = 'db'
ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['DB_FOLDER'] = DB_FOLDER
app.secret_key = 'supersecretkey'

def check_file_existence(path):
  try:
    file_size = os.path.getsize(path)
    if (file_size == 0):
        print("File is empty")
        return False
    else:
        print("File is NOT empty")
        return True
  except FileNotFoundError as e:
      print("File NOT found")
      return False

def endcode_base_64(file):
  try:
    base64_encoded = base64.b64encode(file)
    return base64_encoded.decode('utf-8')
  except:
    flash("Error on converting file")
    
def write_user_data(json_data):
  file_path = f"{app.config['DB_FOLDER']}/db.json"
  try:
    if(check_file_existence(file_path) is False):
      # inicializa arquivo caso vazio ou inexistente
      with open(file_path, 'w', encoding="utf-8") as file_db:
        file_db.write(json.dumps({"user_data": []}))
    
    # carrega arquivo json como dict, adiciona o novo item, converte pra json dnv e escreve no arquivo
    with open(file_path, 'r+', encoding="utf-8") as file_db:
      file_content = json.load(file_db)
      file_content["user_data"].append(json_data)
      file_db.seek(0)
      print(file_db.seek(0))
      json.dump(file_content, file_db, ensure_ascii=False, sort_keys=True, indent=4)
  except:
    flash("Error on saving data")

@app.route("/")
def render_form():
  return render_template('main.html')

@app.route("/", methods=['POST'])
def save_form_data():
  error = None
  success = None
  user_data = {
    'name' : None,
    'age': None,
    'photo' : None
  }
  
  if(request.method == 'POST'):
    if 'photo' not in request.files:
      flash('sem arquivo') 
      redirect(request.url)
      
    req_file = request.files['photo']
    
    if req_file.filename == '':
      flash('Nenhum arquivo selecionado')
      return redirect(request.url)
      
    try:
      user_data['name'] = request.form['name']
      user_data['age'] = request.form['age']
      user_data['photo'] =  endcode_base_64(req_file.read())
      
      # escreve registro no arquivo no db.json
      write_user_data(user_data)

      success = "DADOSSSS!!! 😋😋😋"
    except Exception as e:
      print(e)
      error = "Falha em pegar teus dados :((("
    finally:
      return render_template('main.html', error=error, success=success)
  