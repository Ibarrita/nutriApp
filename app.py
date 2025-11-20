from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)

USUARIOS = {
    "admin@example.com": {
        "nombre": "Admin",
        "contrasena": "secreta",
    }
}

app.config["SECRET_KEY"] = "algo"

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

if __name__ == "__main__":
    app.run(debug=True)