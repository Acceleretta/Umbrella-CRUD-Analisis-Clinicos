from flask import Flask, render_template, request, redirect, flash, url_for

from src.controllers.clientes_controller import *
from src.controllers.estudios_controller import *
from src.controllers.historial_controller import *
from src.controllers.resultados_controller import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ver_cliente')
def ver_cliente():
    clientes = obtener_cliente()
    return render_template("clientes/obtener_cliente.html", clientes=clientes)


@app.route("/eliminar_cliente", methods=["POST"])
def eliminar_cliente():
    borrar_cliente(request.form["id"])
    return redirect("/ver_cliente")


@app.route("/formulario_editar_cliente/<int:idCliente>")
def formulario_editar_cliente(idCliente):
    cliente = obtener_cliente_por_id(idCliente)
    return render_template("clientes/editar_cliente.html", cliente=cliente)


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
    return render_template("clientes/agregar_cliente.html")


@app.route("/guardar_cliente", methods=["POST"])
def guardar_cliente():
    insertar_cliente(request.form["nombre"], request.form["apellido_paterno"], request.form["apellido_materno"],
                     request.form["fecha_nacimiento"], request.form["telefono"], request.form["correo"])
    flash("Cliente guardado exitosamente!", "success")

    return redirect(url_for('formulario_agregar_cliente'))


'''''''''''''''''''''''''''''''''''''''''''''''''''''''Esta parte son funciones de estudio'''''''''''''''''''''''''''''''''''''''''''''''''''''''


@app.route('/ver_estudio')
def ver_estudio():
    estudios = obtener_estudio()
    return render_template("estudios/obtener_estudios.html", estudios=estudios)


@app.route("/formulario_agregar_estudio")
def formulario_agregar_estudio():
    return render_template("estudios/agregar_estudio.html")


@app.route("/guardar_estudio", methods=["POST"])
def guardar_estudio():
    insertar_estudio(request.form["nombre"], request.form["precio"], request.form["rango_inicio"],
                     request.form["rango_fin"])
    flash("Estudio guardado exitosamente!", "success")

    return redirect(url_for('formulario_agregar_estudio'))


@app.route("/eliminar_estudio", methods=["POST"])
def eliminar_estudio():
    borrar_estudio(request.form["id"])
    return redirect("/ver_estudio")


@app.route("/formulario_editar_estudio/<int:idEstudio>")
def formulario_editar_estudio(idEstudio):
    estudio = obtener_estudio_por_id(idEstudio)
    return render_template("estudios/editar_estudio.html", estudio=estudio)


@app.route("/actualizar_estudio", methods=["POST"])
def actualizar_estudio():
    modificar_estudio(request.form["id"], request.form["nombre"], request.form["precio"], request.form["rango_inicio"],
                      request.form["rango_fin"])
    flash("Estudio editado exitosamente!", "success")
    return redirect("/ver_estudio")


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''Parte de orden de analisis'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


@app.route("/ver_clientes_orden")
def ver_clientes_orden():
    clientes = obtener_cliente()
    return render_template("orden_analisis/obtener_cliente_orden.html", clientes=clientes)


@app.route('/formulario_generar_orden/<int:idCliente>')
def formulario_generar_orden(idCliente):
    cliente = obtener_cliente_por_id(idCliente)
    estudios = obtener_estudio()
    return render_template("orden_analisis/generar_orden.html", cliente=cliente, estudios=estudios)


@app.route("/guardar_orden", methods=["POST"])
def guardar_orden():
    id_cliente = request.form["idCliente"]
    nombre_estudio = request.form["nombreEstudio"]
    razon_factura = request.form["razonFactura"]
    estudios = obtener_estudio()
    # Buscar el ID del estudio correspondiente al nombre seleccionado
    id_estudio = None
    for estudio in estudios:
        if estudio[1] == nombre_estudio:
            id_estudio = estudio[0]
            break

    orden_id = generar_orden(id_cliente, id_estudio)
    generar_factura(orden_id, razon_factura)

    return redirect(url_for('ver_clientes_orden'))


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''Historial '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


@app.route('/ver_historial_precios')
def ver_historial_precios():
    precios = obtener_historial_precios()
    return render_template("historial/historial_precios.html", precios=precios)


@app.route('/ver_historial_rangos')
def ver_historial_rangos():
    rangos = obtener_historial_rangos()
    return render_template("historial/historial_rangos.html", rangos=rangos)


@app.route('/ver_historial_resultados')
def ver_historial_resultados():
    resultados = obtener_historial_resultados()
    return render_template("historial/historial_rangos.html", resultados=resultados)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''Resultados '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


@app.route('/ver_ordenes_sin_resultado')
def ver_ordenes_sin_resultado():
    ordenes_sin_resultado = obtener_ordenes_sin_resultados()
    return render_template("resultados/obtener_ordenes_sin_resultado.html", ordenes_sin_resultado=ordenes_sin_resultado)


@app.route('/formulario_generar_resultados/<int:idDetalleOrden>')
def formulario_generar_resultados(idDetalleOrden):
    return render_template("resultados/agregar_resultado.html", idDetalleOrden=idDetalleOrden)


@app.route("/guardar_resultado", methods=["POST"])
def guardar_resultado():
    insertar_resultado(request.form["valor"], request.form["idDetalleOrden"])
    return redirect(url_for('index'))


@app.route("/ver_resultados")
def ver_resultados():
    resultados = obtener_resultados()
    return render_template("resultados/obtener_resultados.html", resultados=resultados)


@app.route("/formulario_editar_resultado/<int:idResultado>")
def formulario_editar_resultado(idResultado):
    resultado = obtener_resultados_por_id(idResultado)
    return render_template("resultados/editar_resultado.html", resultado=resultado)


@app.route("/actualizar_resultado", methods=["POST"])
def actualizar_resultado():
    modificar_resultado(request.form["idResultado"], request.form["idOrden"], request.form["valor"])
    return redirect("/ver_resultados")


app.run(host='0.0.0.0', port=81)
