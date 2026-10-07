# Wokwi ESP32 → pipeline Bài 2 IoT

Tái dựng từ dự án Wokwi của Nam Khanh: https://wokwi.com/projects/477199664093349889
("B23DCAT148 - Bai 2 IoT"). ESP32 + DHT22 + HC-SR04 + LED, publish JSON lên
HiveMQ công cộng, chu kỳ 5 giây.

## File
- `esp32-blink.ino`, `diagram.json`, `libraries.txt` — source gốc từ Wokwi (tải qua API dự án).
- `wokwi_bridge.py` — HiveMQ → Mosquitto nội bộ (chuẩn hóa payload cho collector).
- `mqtt_hivemq_sub.py` — client subscribe HiveMQ, ghi `hivemq_capture.log`.
- `query_esp32.py` — kiểm tra dữ liệu esp32_01 trong InfluxDB.
- `make_figs_wokwi.py` — sinh hình minh chứng (kiến trúc, raw/clean, log).

## Chạy lại
```bash
# Docker Mosquitto + InfluxDB: (đang chạy sẵn) docker compose up -d  [trong iot-lab2-source/iot-lab2]
.venv python collector.py      # nếu chưa chạy
.venv python wokwi_bridge.py   # cầu nối HiveMQ -> Mosquitto
.venv python preprocess.py --watch --minutes 60
streamlit run dashboard.py
```
Mở dự án Wokwi ở trên và bấm Play để thiết bị publish.

