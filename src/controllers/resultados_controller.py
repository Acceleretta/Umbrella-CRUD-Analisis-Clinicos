from src.database.db_mysql import get_connection


def obtener_ordenes_sin_resultados():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_obtener_ordenes_sin_resultados')
            ordes_sin_resultado = cursor.fetchall()
    finally:
        conn.close()

    return ordes_sin_resultado


def insertar_resultado(valor, idDetalleOrden):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_crear_resultado', (valor, idDetalleOrden))
    conn.commit()
    conn.close()


def obtener_resultados():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_obtener_resultados')
            resultados = cursor.fetchall()
    finally:
        conn.close()

    return resultados


def obtener_resultados_por_id(idResultado):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_obtener_resultados_id', (idResultado,))
        resultado = cursor.fetchone()
    conn.commit()
    conn.close()
    return resultado


def modificar_resultado(idResultadoAnalisis, idDetalleOrden, valor):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_actualizar_resultado',
                        (idResultadoAnalisis, idDetalleOrden, valor))
    conn.commit()
    conn.close()
