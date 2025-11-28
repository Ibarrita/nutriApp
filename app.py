from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import requests

# Recordatorio: Redondear los resultados de las calculadoras round()

app = Flask(__name__)

USUARIOS = {
    "admin@example.com": {
        "nombre": "Admin",
        "contrasena": "secreta",
    }
}

app.config["SECRET_KEY"] = "algo"

API = "https://api.spoonacular.com/recipes/"
KEY = "bfb179e20d8e4eb9bafa8bf135f88bca"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signin")
def signin():
    if session.get("logueado") == True:
        session.clear()
        return redirect(url_for("index"))
    return render_template("signin.html")

@app.route("/sesion", methods=["GET", "POST"])
def sesion():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password")
        # Validar datos
        if not email or not password:
            flash("Por favor, ingresa email y contraseña", "error")
        elif email not in USUARIOS or password != USUARIOS[email].get("contrasena"):
            flash("Datos incorrectos", "error")
        else:
            session["email"] = email
            session["contrasena"] = password
            session["logueado"] = True
            flash("Se inicio sesión")
            return redirect(url_for("index"))
    return redirect(url_for("signin"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        edad = request.form["edad"]
        email = request.form["email"]
        password = request.form["password"]
        objetivos = request.form["objetivos"]
        restricciones = request.form["restricciones"]
        experiencia = request.form["experiencia"]
        if not email or not password:
            flash("Falta el correo electrónico o la contraseña", "error")
        elif not edad:
            flash("Falta la edad", "error")
        else:
            flash("Registro exitoso")
            edad = int(edad)
            return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/articulos")
def articulos():
    return render_template("articulos.html")

@app.route("/herramientas")
def herramientas():
    return render_template("herramientas.html")

@app.route("/herramientas/imc", methods=["GET", "POST"])
def imc():
    imc = None
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        if not peso or not altura:
            flash("Falta el peso o la altura.", "error")
        else:
            imc = peso / (altura / 100) ** 2
    return render_template("/herramientas/imc.html", imc=imc)

@app.route("/herramientas/tmb", methods=["GET", "POST"])
def tmb():
    tmb = None
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        edad = int(request.form.get("edad"))
        genero = request.form.get("genero")
        if not peso or not altura:
            flash("Falta el peso o la altura.", "error")
        elif not edad:
            flash("Falta la edad.", "error")
        else:
            if genero == "m":
                tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
            elif genero == "f":
                tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161
    return render_template("/herramientas/tmb.html", tmb=tmb)

@app.route("/herramientas/gct", methods=["GET", "POST"])
def gct():
    gct = None
    if request.method == "POST":
        peso = float(request.form.get("peso"))
        altura = float(request.form.get("altura"))
        edad = int(request.form.get("edad"))
        genero = request.form.get("genero")
        actividad = request.form.get("actividad")
        if not peso or not altura:
            flash("Falta el peso o la altura.", "error")
        elif not edad:
            flash("Falta la edad.", "error")
        else:
            if genero == "m":
                tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
                if actividad == "leve":
                    gct = tmb * 1.55
                elif actividad == "moderada":
                    gct = tmb * 1.84
                elif actividad == "intensa":
                    gct = tmb * 2.2
            elif genero == "f":
                tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161
                if actividad == "leve":
                    gct = tmb * 1.55
                elif actividad == "moderada":
                    gct = tmb * 1.84
                elif actividad == "intensa":
                    gct = tmb * 2.2
    return render_template("/herramientas/gct.html", gct=gct)

@app.route("/recetas")
def recetas():
    return render_template("recetas.html")

@app.route("/search", methods=["POST"])
def search():
    recipe_name = request.form.get("recipe", "").strip().lower()
    
    if not recipe_name:
        flash("Por favor, ingresa un alimento", "error")
        return redirect(url_for("recetas"))
    try:
        response = requests.get(f"{API}/complexSearch?apiKey={KEY}&query={recipe_name}&maxFat=25&number=1")
        
        if response.status_code == 200:
            recipe_data = response.json()
            results = recipe_data.get("results", [])
            if not results:
                flash("No se encontró el alimento", "error")
                return redirect(url_for("recetas"))
            resultados = results[0]
            recipe_info = {
                "title": resultados.get("title"),
                "image": resultados.get("image")
            }
            return render_template("alimento.html", recipe=recipe_info)
        else:
            flash("Error al contactar con la API", "error")
            return redirect(url_for("recetas"))
    except requests.exceptions.RequestException as e:
        flash("No se pudo contactar con la API", "error")
        return redirect(url_for("recetas"))
    
@app.route("/analizador")
def analizador():
    return render_template("analizador.html")

@app.route("/analizar", methods=["GET", "POST"])
def analizar():
    analisis = None
    error = None
    if request.method == "POST":
        tipo_analisis = request.form.get("tipo_analisis")
        
        if tipo_analisis == "manual":
            titulo = request.form.get("titulo", "")
            porciones = request.form.get("porciones", "")
            ingredientes = request.form.get("ingredientes", "").split("\n")
            
            url = f"{API}/analyze"
            params = {"apiKey": KEY,
                    "includeNutrition": True,
                    "language": "en"}
            
            data = {
                "title": titulo,
                "ingredients": [ing for ing in ingredientes if ing.strip()],
                "servings": porciones,
            }
            
            try:
                response = requests.post(url, params=params, json=data)
                analisis = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Error analizando receta: {e}")
                return None
            if not analisis:
                error = "No se pudo analizar la receta. Verifica los datos e intenta nuevamente"
        return render_template("analizador.html", analisis=analisis, error=error)

if __name__ == "__main__":
    app.run(debug=True)