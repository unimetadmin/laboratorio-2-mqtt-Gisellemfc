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
	client = paho.mqtt.client.Client("Olla", False)
	client.qos = 0
	client.connect(host='localhost')

	#Datos olla
	mensaje = ""
	
	#Hora base
	query = """SELECT fecha_temperatura FROM public.cocina_olla ORDER BY id DESC LIMIT 1;"""
	horaBase= db_script.select_ultima_fecha(query)

	while(True):

		#Manejo del tiempo temperatura
		horaBase = horaBase + datetime.timedelta(seconds=1)

		#Temperatura
		temperatura = int(np.random.uniform(0, 151))
		
		if(temperatura >= 100):
			mensaje = "El agua ya hirvio"
		else:
			mensaje = "El agua no ha hervido"

        #Mensaje
		payload = {
			"fecha_temperatura": str(horaBase),
			"temperatura_olla": str(temperatura),
			"mensaje": mensaje
		}

		#Canal donde publica
		client.publish('casa/cocina/olla',json.dumps(payload),qos=0)		
		print(payload)

        #Tiempo entre simulacióm
		time.sleep(1)

		#Reducir el tiempo que queda de uso de la olla
		# uso_olla -= 1

if __name__ == '__main__':
	main()
	sys.exit(0)