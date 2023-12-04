from src.database.db_mysql import get_connection


def obtener_hitorial_precios():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_obtener_cliente')
            clientes = cursor.fetchall()
    finally:
        conn.close()

    return clientes
