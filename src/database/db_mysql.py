import pymysql


def get_connection():
    return pymysql.connect(
        host='localhost',  # Cambia esto por la dirección de tu base de datos
        user='root',
        password='root',
        db='umbrelladb',
    )
