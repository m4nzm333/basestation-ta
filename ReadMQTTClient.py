import paho.mqtt.client as mqtt
import datetime as datetime

# MQTT Setting
MQTT_Broker = "192.168.1.9"
MQTT_Port = 1883
Keep_Alive_Interval = 45
MQTT_Topic = "Temperatur"

mqttc = mqtt.Client("Detektor Temperatur")
# Read Data Function
def on_message(mosq, obj, msg):
    print("============================")
    print("MQTT Data Received On " + str(datetime.datetime.now()))
    print("Data : " + msg.payload)
    print("============================")
    print("\n")

def on_subscribe(mosq, obj, mid, granted_qos):
    pass

def on_connect(client, userdata, flag, rc):
    if rc==0:
        print("Connection successful\n")
    if rc==1:
        print("Connection refused - incorrect protocol version\n")
    if rc==2:
        print("Connection refused - invalid client identifier\n")
    if rc==3:
        print("Connection refused - server unavailable\n")
    if rc==4:
        print("Connection refused - not authorised\n")

print("Connection to Broker with Address " + str(MQTT_Broker) + ":" + str(MQTT_Port))
print("==================================")
print("\nSubscribe on Topic = " + MQTT_Topic + "\n")

# Assign Event Callbacks
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_connect = on_connect

# Connect
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
mqttc.subscribe(MQTT_Topic)

#Continue the network loop
mqttc.loop_forever()