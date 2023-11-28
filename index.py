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


@app.route("/formulario_editar_cliente/<int:idCliente>")
def formulario_editar_cliente(idCliente):
    cliente = obtener_cliente_por_id(idCliente)
    return render_template("editar_cliente.html", cliente=cliente)


'''@app.route("/buscar_cliente", methods=["GET", "POST"])
def buscar_cliente():
    if request.method == "POST":
        # Obtener parámetros del formulario de búsqueda
        nombre = request.form.get("nombre") or None
        apellido_paterno = request.form.get("apellido_paterno") or None
        apellido_materno = request.form.get("apellido_materno") or None

        # Realizar la búsqueda y obtener resultados
        clientes = buscar_clientes(nombre, apellido_paterno, apellido_materno)

        # Flash y redirigir si es necesario
        print(clientes)  # Agrega esta línea para imprimir los resultados en la consola del servidor

        return render_template("obtener_cliente.html", clientes=clientes)

    # Resto de la lógica para el método GET
    clientes = obtener_cliente()
    print(clientes)  # Agrega esta línea para imprimir los resultados en la consola del servidor
    return render_template("obtener_cliente.html", clientes=clientes)'''



@app.route("/actualizar_cliente", methods=["POST"])
def actualizar_cliente():
    modificar_cliente(request.form["id"], request.form["nombre"], request.form["apellido_paterno"],
                      request.form["apellido_materno"], request.form["fecha_nacimiento"], request.form["telefono"],
                      request.form["correo"])
    flash("Cliente editado exitosamente!", "success")
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
