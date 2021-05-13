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

	#Datos contador
	mensaje = ""
	
	#Hora base
	query = """SELECT fecha_conteo FROM public.sala_contador_personas ORDER BY id DESC LIMIT 1;"""
	horaBase= db_script.select_ultima_fecha(query)

	while(True):

		#Manejo del tiempo conteo
		horaBase = horaBase + datetime.timedelta(minutes=1)	

		#Cantidad de personas en la sala
		cantidad_personas = int(np.random.uniform(0, 11))
		
		if(cantidad_personas > 5):
			mensaje = "Alerta COVID, hay muchas personas en la sala"
		else:
			mensaje = "Hay pocas personas en la sala, no hay peligro de COVID"

        #Mensaje
		payload = {
			"fecha_conteo": str(horaBase),
			"cantidad_personas": str(cantidad_personas),
			"mensaje": mensaje
		}

		#Canal donde publica
		client.publish('casa/sala/contador_personas',json.dumps(payload),qos=0)		
		print(payload)

        #Tiempo entre simulacióm
		time.sleep(1)

if __name__ == '__main__':
	main()
	sys.exit(0)