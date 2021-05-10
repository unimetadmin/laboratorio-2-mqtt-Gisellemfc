import psycopg2
from psycopg2 import Error
import pandas as pd

def connection():
    connection = psycopg2.connect(
        user = "zaxrjvmg",
        password = "QvpLV66kCbNLGIgV_RDi6T-0nWyWGpfc",
        host = "queenie.db.elephantsql.com",
        port = "5432",
        database = "zaxrjvmg"
    )
    return connection

def insertar_dos_datos(query, dato_uno, dato_dos):

    try:

        #Conexión con la BD
        conexion = connection()
        cursor = conexion.cursor()

        #Query para insertar
        cursor.execute(query,(dato_uno, dato_dos))

        #Guardar en la BD
        conexion.commit()

        #Cerrar conexión
        close_connection(conexion)

    except (Exception, psycopg2.Error) as error:

        print('Error insertando la data',error)

def insertar_tres_datos(query, dato_uno, dato_dos, dato_tres):

    try:

        #Conexión con la BD
        conexion = connection()
        cursor = conexion.cursor()

        #Query para insertar
        cursor.execute(query,(dato_uno, dato_dos, dato_tres))

        #Guardar en la BD
        conexion.commit()

        #Cerrar conexión
        close_connection(conexion)

    except (Exception, psycopg2.Error) as error:

        print('Error insertando la data',error)

def select_ultima_fecha(query):

    try:

        #Conexión con la BD
        conexion = connection()
        cursor = conexion.cursor()

        #Query para traer la ultima fecha
        cursor.execute(query)

        ultima_fecha = cursor.fetchone()

        #Cerrar conexión
        close_connection(conexion)

        #Devolver la ultima fecha
        return ultima_fecha[0]

    except (Exception, psycopg2.Error) as error:

        print('Error buscando la data',error)

def close_connection(connection):
    if connection:
        connection.close()