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

if __name__ == "__main__":
    app.run(debug=True)