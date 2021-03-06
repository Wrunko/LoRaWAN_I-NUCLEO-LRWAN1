# -*- coding: utf-8 -*-
"""
Created on Fri May 17 15:07:54 2019

@author: alexa
"""

import paho.mqtt.client as mqtt
import mysql.connector as mysql


############ CODE MYSQL ############

mydb = mysql.connect(host="localhost or other address", user="your_username", passwd="your_psswd", database="your_namedatabase")
mycursor = mydb.cursor()

sql = "INSERT INTO my_table (my_attribute) VALUES (%s)"

############ CODE MQTT PAHO ############

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("MQTT: Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    print(msg.topic+" "+str(msg.payload))
    val = (msg.payload)
    mycursor.execute(sql, (val,))
    mydb.commit()




client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("your_broker_address", "broker_port", 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

