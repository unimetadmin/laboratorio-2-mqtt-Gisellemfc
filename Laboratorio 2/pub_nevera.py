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
	client = paho.mqtt.client.Client("Nevera", False)
	client.qos = 0
	client.connect(host='localhost')

	#Datos nevera
	media = 10
	desviacion = 2
	medidor = np.random.normal(media, desviacion)
	flagHielo = False
	
	# Hora base
	query = """SELECT fecha_temperatura FROM public.cocina_nevera_temperatura ORDER BY id DESC LIMIT 1;"""
	horaBase= db_script.select_ultima_fecha(query)

	while(medidor>0):

		#Manejo del tiempo temperatura
		horaBase = horaBase + datetime.timedelta(minutes=5)	

		#Temperatura
		temperatura = int(np.random.uniform(8, 13))
		
        #Mensaje
		payload = {
			"fecha_temperatura": str(horaBase),
			"temperatura_nevera": str(temperatura)
		}

		#Canal donde publica
		client.publish('casa/cocina/temperatura_nevera',json.dumps(payload),qos=0)		
		print(payload)

        #Tiempo entre simulacióm
		time.sleep(1)
		
		if(horaBase.minute % 10 == 0):

			#Hielo
			hielo = int(np.random.uniform(0, 10))

			#Mensaje
			payload = {
				"fecha_hielo": str(horaBase),
				"hielo": str(hielo)
			}

			#Canal donde publica
			client.publish('casa/cocina/hielo_nevera',json.dumps(payload),qos=0)		
			print(payload)

        #Tiempo entre simulacióm
		time.sleep(1)

		#Reducir el tiempo de actividad del medidor de la nevera
		# medidor -= 1

		#VER QUE HACER CON EL MEDIDOR XD
        
if __name__ == '__main__':
	main()
	sys.exit(0)