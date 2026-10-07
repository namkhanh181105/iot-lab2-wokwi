# Cau noi: HiveMQ (Wokwi ESP32) -> Mosquitto local (dinh dang pipeline Bai 2).
import json, time
import paho.mqtt.client as mqtt

SRC_HOST, SRC_TOPIC = "broker.hivemq.com", "lab2/sensors/esp32_01/data"
DST_HOST, DST_PORT = "localhost", 1883
DEVICE = "esp32_01"

def on_connect(c, u, f, rc, props=None):
    print("HiveMQ connected rc=", rc, flush=True)
    c.subscribe(SRC_TOPIC, qos=1)

dst = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="wokwi-bridge-dst")
dst.connect(DST_HOST, DST_PORT, 60)
dst.loop_start()

def on_message(c, u, msg):
    try:
        w = json.loads(msg.payload)
    except Exception:
        return
    out = {"device_id": DEVICE,
           "ts_ms": int(time.time() * 1000),
           "seq": int(w.get("sequence", 0)),
           "temperature": float(w.get("temperature", 0.0)),
           "humidity": float(w.get("humidity", 0.0))}
    dst.publish(f"iot/lab2/{DEVICE}/telemetry", json.dumps(out), qos=1)
    print("bridge ->", json.dumps(out), flush=True)

src = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="wokwi-bridge-src")
src.on_connect = on_connect
src.on_message = on_message
src.connect(SRC_HOST, 1883, 60)
src.loop_forever()
