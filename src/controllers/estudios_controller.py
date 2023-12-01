from src.database.db_mysql import get_connection


def insertar_estudio(nombreEstudio, costoEstudio, rangoIncioEstudio, rangoFinEstudio):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_insertar_estudio',
                        (nombreEstudio, costoEstudio, rangoIncioEstudio, rangoFinEstudio))
    conn.commit()
    conn.close()


def obtener_estudio():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.callproc('sp_obtener_estudio')
            estudios = cursor.fetchall()
    finally:
        conn.close()

    return estudios


def borrar_estudio(idEstudio):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_borrar_estudio', idEstudio)
    conn.commit()
    conn.close()


def obtener_estudio_por_id(idEstudio):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_obtener_estudio_id', (idEstudio,))
        estudio = cursor.fetchone()
    conn.commit()
    conn.close()
    return estudio


def modificar_estudio(idEstudio, nombreEstudio, costoEstudio, rangoIncioEstudio, rangoFinEstudio):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_actualizar_estudio',
                        (idEstudio, nombreEstudio, costoEstudio, rangoIncioEstudio, rangoFinEstudio))
    conn.commit()
    conn.close()


'''def buscar_clientes(nombreCliente=None, apellidoPatCliente=None, apellidoMatCliente=None):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.callproc('sp_buscar_clientes',
                        (nombreCliente, apellidoPatCliente, apellidoMatCliente))
        clientes = cursor.fetchall()
    conn.close()
    return clientes'''
