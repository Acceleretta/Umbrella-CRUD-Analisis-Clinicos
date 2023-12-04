from src.database.db_mysql import get_connection


def obtener_historial_precios():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_obtener_historial_precios')
            historial_precios = cursor.fetchall()
    finally:
        conn.close()

    return historial_precios


def obtener_historial_rangos():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_obtener_historial_rangos')
            historial_rangos = cursor.fetchall()
    finally:
        conn.close()

    return historial_rangos


def obtener_historial_precios():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_obtener_historial_precios')
            historial_precios = cursor.fetchall()
    finally:
        conn.close()

    return historial_precios

def obtener_historial_resultados():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_obtener_historial_resultados')
            historial_resultados = cursor.fetchall()
    finally:
        conn.close()

    return historial_resultados