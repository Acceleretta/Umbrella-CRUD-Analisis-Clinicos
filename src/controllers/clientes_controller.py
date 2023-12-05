from src.database.db_mysql import get_connection


def insertar_cliente(nombreCliente, apellidoPatCliente, apellidoMatCliente, nacimientoCliente, telefonoCliente,
                     correoCliente):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_insertar_cliente',
                        (nombreCliente, apellidoPatCliente, apellidoMatCliente, nacimientoCliente, telefonoCliente,
                         correoCliente))
    conn.commit()
    conn.close()


def buscar_clientes(nombreCliente=None, apellidoPatCliente=None, apellidoMatCliente=None):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_buscar_clientes',
                        (nombreCliente, apellidoPatCliente, apellidoMatCliente))
        clientes = cursor.fetchall()
    conn.close()
    return clientes


def obtener_cliente():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_obtener_cliente')
            clientes = cursor.fetchall()
    finally:
        conn.close()

    return clientes


def borrar_cliente(idCliente):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_borrar_cliente', idCliente)
    conn.commit()
    conn.close()


def obtener_cliente_por_id(idCliente):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_obtener_cliente_id', (idCliente,))
        cliente = cursor.fetchone()
    conn.commit()
    conn.close()
    return cliente


def modificar_cliente(idCliente, nombreCliente, apellidoPatCliente, apellidoMatCliente, nacimientoCliente,
                      telefonoCliente, correoCliente):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_actualizar_cliente',
                        (idCliente, nombreCliente, apellidoPatCliente, apellidoMatCliente, nacimientoCliente,
                         telefonoCliente,
                         correoCliente))
    conn.commit()
    conn.close()


def generar_orden(idCliente, idEstudio):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_generar_orden', (idCliente, idEstudio))
    conn.commit()
    conn.close()


def generar_factura(razonFactura):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_crear_factura', (razonFactura,))
    conn.commit()
    conn.close()


def obtener_factura():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_obtener_facturas')
            facturas = cursor.fetchall()
    finally:
        conn.close()

    return facturas
