import sys
sys.path.insert(0, r"C:\Users\ADMIN\Downloads\iot-lab2-source\iot-lab2")
from common import db, BUCKET, ORG

q = f'''from(bucket:"{BUCKET}") |> range(start: -2h)
|> filter(fn:(r) => r._measurement == "sensor_raw" and r.device_id == "esp32_01")
|> filter(fn:(r) => r._field == "temperature" or r._field == "humidity" or r._field == "latency_ms")
|> sort(columns:["_time"], desc:false)'''

with db() as c:
    n = 0
    for t in c.query_api().query(q, org=ORG):
        for r in t.records:
            print(r.get_time().strftime("%H:%M:%S"), r.get_field(), round(r.get_value(), 3))
            n += 1
    print("TOTAL esp32_01 sensor_raw points:", n)
