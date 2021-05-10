import ssl
import sys
import json
import random
import time
import paho.mqtt.client
import paho.mqtt.publish
import numpy as np
import datetime
import psycopg2
import db_script
import json

def on_connect(client, userdata, flags, rc):
	print('conectado publicador')

def main():
	
	#Info publicador
	client = paho.mqtt.client.Client("ContadorPersonas", False)
	client.qos = 0
	client.connect(host='localhost')

	#Datos tanque
	mensaje = ""
	agua_disponible = 100
	media_salida = 0.1
	desviacion_salida = 0.05
	media_entrada = 0.20
	desviacion_entrada = 0.05
	agua_entrada = 0
	agua_salida = 0
	
	#Hora base
	query = """SELECT fecha_medicion FROM public.bano_tanque ORDER BY id DESC LIMIT 1;"""
	horaBase= db_script.select_ultima_fecha(query)

	while(True):

		#Manejo del tiempo conteo
		horaBase = horaBase + datetime.timedelta(minutes=10)	

		#Agua de salida
		agua_salida = round(np.random.normal(media_salida,desviacion_salida), 2) * 100

		if(agua_disponible - agua_salida < 0.00):  

			agua_disponible = 0

		else:

			agua_disponible = round(agua_disponible - agua_salida, 2)

		#Calculo de agua disponible
		if(horaBase.minute == 30 or horaBase.minute == 00):

			agua_entrada = round(np.random.normal(media_entrada,desviacion_entrada), 2) * 100
		
			if(agua_disponible + agua_entrada > 100.00):  

				agua_disponible = 100

			else:

				agua_disponible = round(agua_disponible + agua_entrada, 2)
			
		#Manejo de la alerta
		if(agua_disponible == 0):

			mensaje = "Alerta, no hay agua"

		elif(agua_disponible <= 50):

			mensaje = "Alerta, queda menos de medio tanque"

		else:

			mensaje = "Tenemos agua para rato"
		
        #Mensaje
		payload = {
			"fecha_medicion": str(horaBase),
			"agua_disponible": str(agua_disponible),
			"mensaje": mensaje
		}

		#Canal donde publica
		client.publish('casa/bano/nivel_tanque',json.dumps(payload),qos=0)		
		print(payload)

        #Tiempo entre simulación
		time.sleep(1)

if __name__ == '__main__':
	main()
	sys.exit(0)