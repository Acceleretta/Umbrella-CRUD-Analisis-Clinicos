from flask import Flask, render_template, request, redirect, flash, url_for

from src.controllers.clientes_controller import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ver_cliente')
def ver_cliente():
    clientes = obtener_cliente()
    return render_template("obtener_cliente.html", clientes=clientes)


@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_cliente():
    borrar_cliente(request.form["id"])
    return redirect("/ver_cliente")


@app.route("/formulario_editar_cliente/<int:id>")
def editar_cliente(idCliente):
    cliente = obtener_cliente_por_id(id)
    return render_template("editar_cliente.html", cliente=cliente)


@app.route("/actualizar_juego", methods=["POST"])
def actualizar_cliente():
    modificar_cliente(request.form["id"], request.form["nombre"], request.form["apellido_paterno"],
                      request.form["apellido_materno"], request.form["fecha_nacimiento"], request.form["telefono"],
                      request.form["correo"])
    return redirect("/ver_cliente")


@app.route('/formulario_agregar_cliente')
def formulario_agregar_cliente():
    return render_template("agregar_cliente.html")


@app.route("/guardar_cliente", methods=["POST"])
def guardar_cliente():
    insertar_cliente(request.form["nombre"], request.form["apellido_paterno"], request.form["apellido_materno"],
                     request.form["fecha_nacimiento"], request.form["telefono"], request.form["correo"])
    flash("Cliente guardado exitosamente!", "success")

    return redirect(url_for('formulario_agregar_cliente'))


app.run(host='0.0.0.0', port=81)
