import ssl
import sys
import json
import random
import time
import paho.mqtt.client
import paho.mqtt.publish
import numpy as np
import datetime
import requests
import psycopg2
import db_script
import json

def on_connect(client, userdata, flags, rc):
	print('conectado publicador')

def get_weather():

	api_key = "83fc9089af79b5337705036f8fe7219f"
	lat = "10.502780"
	lon = "-66.919052"
	url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

	response = requests.get(url)
	data = json.loads(response.text)
	current = data["current"]["temp"]

	return current

def main():

	#Info publicador
	client = paho.mqtt.client.Client("Alexa", False)
	client.qos = 0
	client.connect(host='localhost')

	#Datos Alexa
	temperatura_caracas = get_weather()
	flag_primero = True
	flag_operacion = True
	
	#Hora base
	query = """SELECT fecha_alexa FROM public.sala_alexa_echo ORDER BY id DESC LIMIT 1;"""
	horaBase= db_script.select_ultima_fecha(query)

	while(True):

		#Manejo del tiempo temperatura
		horaBase = horaBase + datetime.timedelta(minutes=30)	

		#Temperatura
		if(not flag_primero):
			if(flag_operacion):

				temperatura_caracas = round(temperatura_caracas + np.random.random(), 2)
			
			else:

				temperatura_caracas = round(temperatura_caracas - np.random.random(), 2)
					
        #Mensaje
		payload = {
			"fecha_temperatura": str(horaBase),
			"temperatura_caracas": str(temperatura_caracas)
		}

		#Canal donde publica
		client.publish('casa/sala/alexa_echo',json.dumps(payload),qos=0)		
		print(payload)

        #Tiempo entre simulacióm
		time.sleep(2)

		#Cambiar valor de las banderas
		flag_primero = False
		flag_operacion = not flag_operacion	
	


if __name__ == '__main__':
	main()
	sys.exit(0)