from flask import Flask, render_template, request, redirect, url_for, session, flash
import json, os, random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta_super_segura"  # Necesario para sesiones

# Archivos JSON
DATA_FILE = "Inventario/inventario.json"
USERS_FILE = "Inventario/usuarios.json"

# ---------------------------
# Inicializar JSON limpio en Render
# ---------------------------
if "RENDER" in os.environ:  # Render define esta variable de entorno
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write("{}")  # Inventario vacío
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "admin": {"password": "admin123"},
                    "samuel": {"password": "1234"},
                    "eduar": {"password": "abcd"}
                },
                f,
                indent=4,
                ensure_ascii=False
            )

# -------- utilidades --------
def cargar():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def guardar(inv):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(inv, f, indent=4, ensure_ascii=False)

def generar_tocken(inv):
    while True:
        t = f"{random.randint(0, 9999):04d}"
        if t not in inv:
            return t

def cargar_usuarios():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# -------- rutas --------
@app.route("/")
def index():
    if "usuario" not in session:
        return redirect(url_for("login"))

    inv = cargar()
    return render_template("index.html", inventario=inv, usuario=session["usuario"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        usuarios = cargar_usuarios()

        if username in usuarios and usuarios[username]["password"] == password:
            session["usuario"] = username
            return redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
            return redirect(url_for("login"))  # ⬅️ Redirect en vez de render

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

@app.route("/agregar", methods=["POST"])
def agregar():
    if "usuario" not in session:
        return redirect(url_for("login"))

    inv = cargar()

    producto = request.form.get("nombre") or request.form.get("producto")
    marca = request.form.get("marca")
    seccion = request.form.get("seccion")
    cantidad = request.form.get("cantidad")
    precio = request.form.get("precio")

    if not all([producto, marca, seccion, cantidad, precio]):
        return "Faltan campos en el formulario.", 400

    tocken = generar_tocken(inv)
    inv[tocken] = {
        "producto": producto,
        "marca": marca,
        "seccion": seccion,
        "cantidad": int(cantidad),
        "precio": float(precio),
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    guardar(inv)
    return redirect(url_for("index"))

@app.route("/eliminar/<tocken>")
def eliminar(tocken):
    if "usuario" not in session:
        return redirect(url_for("login"))

    inv = cargar()
    if tocken in inv:
        del inv[tocken]
        guardar(inv)
    return redirect(url_for("index"))

@app.route("/editar/<tocken>", methods=["GET", "POST"])
def editar(tocken):
    if "usuario" not in session:
        return redirect(url_for("login"))

    inv = cargar()

    if tocken not in inv:
        return "Producto no encontrado", 404

    item = inv[tocken]

    if request.method == "POST":
        item["producto"] = request.form["nombre"]
        item["marca"] = request.form["marca"]
        item["seccion"] = request.form["seccion"]
        item["cantidad"] = int(request.form["cantidad"])
        item["precio"] = float(request.form["precio"])

        inv[tocken] = item
        guardar(inv)
        return redirect(url_for("index"))

    return render_template("editar.html", item=item, tocken=tocken)

# -------- Exportar a Excel --------
import pandas as pd
from flask import send_file

@app.route("/exportar")
def exportar():
    if "usuario" not in session:
        return redirect(url_for("login"))

    inv = cargar()
    if not inv:
        return "Inventario vacío", 400

    df = pd.DataFrame(inv).T  # Transponer para que cada fila sea un producto
    file_path = "Inventario/inventario.xlsx"
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
