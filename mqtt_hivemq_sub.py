# Subscribe HiveMQ cong cong, thu du lieu Wokwi ESP32 publish.
import paho.mqtt.client as mqtt
import time, sys

TOPIC = "lab2/sensors/esp32_01/data"
out = open("hivemq_capture.log", "a", encoding="utf-8")

def on_connect(c, u, f, rc):
    print("connected rc=", rc, flush=True)
    c.subscribe(TOPIC, qos=1)

def on_message(c, u, msg):
    line = "[%s] %s" % (time.strftime("%H:%M:%S"), msg.payload.decode("utf-8", "replace"))
    print(line, flush=True)
    out.write(line + "\n")
    out.flush()

cl = mqtt.Client(client_id="cap-" + str(int(time.time())))
cl.on_connect = on_connect
cl.on_message = on_message
cl.connect("broker.hivemq.com", 1883, 30)
cl.loop_forever()
