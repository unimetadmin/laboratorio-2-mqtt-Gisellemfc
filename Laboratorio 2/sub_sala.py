import sys
import paho.mqtt.client
import psycopg2
import db_script
import json

def on_connect(client, userdata, flags, rc):
	print('connected (%s)' % client._client_id)
	client.subscribe(topic='casa/sala/#', qos=2)

def on_message(client, userdata, message):

	try:

		if(message.topic == "casa/sala/contador_personas"):

			query = """INSERT INTO public.sala_contador_personas(fecha_conteo, cantidad_personas, mensaje) VALUES (%s, %s, %s);"""
			db_script.insertar_tres_datos(query, json.loads(message.payload)["fecha_conteo"], json.loads(message.payload)["cantidad_personas"], json.loads(message.payload)["mensaje"])

		else:

			query = """INSERT INTO public.sala_alexa_echo(fecha_alexa, temperatura_caracas) VALUES (%s, %s);"""
			db_script.insertar_dos_datos(query, json.loads(message.payload)["fecha_temperatura"], json.loads(message.payload)["temperatura_caracas"])
		
	except (Exception, psycopg2.Error) as error:

		print("Error while connecting to PostgreSQL", error)

	finally:

		print('------------------------------')
		print('topic: %s' % message.topic)
		print('payload: %s' % message.payload)
		print('qos: %d' % message.qos)

def main():
	client = paho.mqtt.client.Client(client_id='sala-subs', clean_session=False)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(host='127.0.0.1', port=1883)
	client.loop_forever()

if __name__ == '__main__':
	main()

sys.exit(0)