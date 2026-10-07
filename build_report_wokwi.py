# -*- coding: utf-8 -*-
"""Bao cao Bai thuc hanh 2 IoT - tich hop thiet bi Wokwi ESP32."""
import os
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

EV = r"C:\Users\ADMIN\Downloads\wokwi_lab2\report_evidence"
EV2 = r"C:\Users\ADMIN\Downloads\iot-lab2-source\report_evidence"
OUT = r"C:\Users\ADMIN\Downloads\BaoCao_Wokwi_Bai2_IoT.docx"

doc = Document()
st = doc.styles['Normal']
st.font.name = 'Times New Roman'; st.font.size = Pt(12.5)
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
for s in doc.sections:
    s.top_margin = Cm(1.8); s.bottom_margin = Cm(1.8)
    s.left_margin = Cm(2.5); s.right_margin = Cm(2)

def h(text, size=13.5, space_before=8):
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text); r.bold = True; r.font.size = Pt(size); r.font.name = 'Times New Roman'
    return p

def para(text, italic=False, size=12.5):
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.05
    r = p.add_run(text); r.italic = italic; r.font.size = Pt(size)
    return p

def code(text):
    p = doc.add_paragraph(); p.paragraph_format.left_indent = Cm(0.6)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text); r.font.name = 'Consolas'; r.font.size = Pt(9.5)

def bullets(items):
    for it in items:
        p = doc.add_paragraph(style='List Bullet'); p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.1
        p.add_run(it).font.size = Pt(12.5)

def numbered(items):
    for it in items:
        p = doc.add_paragraph(style='List Number'); p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.1
        p.add_run(it).font.size = Pt(12.5)

def img(path, caption, width=4.9):
    if not os.path.exists(path):
        para('[Thieu anh: %s]' % path); return
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(1)
    p.add_run().add_picture(path, width=Inches(width))
    c = doc.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_after = Pt(6)
    r = c.add_run(caption); r.italic = True; r.font.size = Pt(10)

def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, hd in enumerate(headers):
        cell = t.rows[0].cells[i]; cell.text = ''
        r = cell.paragraphs[0].add_run(hd); r.bold = True; r.font.size = Pt(10.5)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ''
            cells[i].paragraphs[0].add_run(str(v)).font.size = Pt(10.5)
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows: row.cells[i].width = Cm(w)
    return t

# ===================== TIEU DE =====================
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('BÁO CÁO BÀI THỰC HÀNH SỐ 2'); r.bold = True; r.font.size = Pt(15)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(6)
r = p.add_run('THU THẬP, LƯU TRỮ VÀ TIỀN XỬ LÝ DỮ LIỆU IoT'); r.bold = True; r.font.size = Pt(13)
table(['Học phần: IoT và Ứng dụng (INT14149)', 'Sinh viên: Trần Bách Thăng — MSSV: 23162094'],
      [['Ngày thực hiện: 07/10/2026', 'Lớp: B23DCAT148 — Khoa Công nghệ Thông tin (HCMUTE)']],
      widths=[7.5, 7.5])
para('Ghi chú: tầng thiết bị dùng đúng firmware do sinh viên viết trên Wokwi (mã dự án 477199664093349889), '
     'được chạy mô phỏng thật và minh chứng bằng ảnh chụp màn hình. Phần lưu trữ – tiền xử lý – dashboard chạy '
     'bằng Docker Mosquitto + InfluxDB + Streamlit trên máy. Nhiệt độ/độ ẩm do cảm biến DHT22 của Wokwi sinh ra '
     'là dữ liệu mô phỏng, được nêu rõ để phân biệt với cảm biến vật lý.', italic=True, size=10.5)

# ===================== 1. MUC TIEU =====================
h('1. Mục tiêu', 13.5)
bullets([
    'Xây dựng pipeline thu thập dữ liệu cảm biến thời gian thực qua MQTT (publish/subscribe).',
    'Triển khai lưu trữ chuỗi thời gian (InfluxDB 2.x) kèm vùng đệm bền vững cục bộ (SQLite outbox).',
    'Tiền xử lý dữ liệu thô: làm sạch, phát hiện bất thường (IQR), resampling, tạo đặc trưng và chuẩn hóa.',
    'Xây dựng dashboard giám sát real-time; đo và phân tích độ trễ, vấn đề lưu trữ; đề xuất cải tiến.',
])

# ===================== 2. KIEN TRUC =====================
h('2. Sơ đồ kiến trúc hệ thống', 13.5)
para('Hệ thống gồm thiết bị ESP32 mô phỏng trên Wokwi publish dữ liệu JSON lên MQTT broker HiveMQ công cộng; '
     'một tiến trình bridge đăng ký nhận lại bản tin và chuyển vào Mosquitto nội bộ để collector kiểm tra hợp lệ, '
     'đệm rồi ghi InfluxDB; preprocess đọc dữ liệu thô và ghi measurement đã làm sạch; dashboard đọc cả hai.')
img(os.path.join(EV, 'fig_arch_wokwi.png'),
    'Hình 1. Kiến trúc tích hợp: thiết bị Wokwi → HiveMQ → bridge → Mosquitto → collector → InfluxDB → tiền xử lý → dashboard.', 5.5)
table(['Khối', 'Công nghệ', 'Nhiệm vụ'],
      [['Thiết bị', 'Wokwi ESP32 + DHT22 + HC-SR04', 'Đọc cảm biến, publish JSON lên HiveMQ mỗi 5 giây'],
       ['Broker công cộng', 'HiveMQ (broker.hivemq.com:1883)', 'Nhận bản tin từ thiết bị, topic lab2/sensors/...'],
       ['Bridge', 'Python paho-mqtt', 'Subscribe HiveMQ, chuẩn hóa payload, publish vào Mosquitto nội bộ'],
       ['Broker nội bộ', 'Eclipse Mosquitto 2', 'Topic iot/lab2/<id>/telemetry, cổng 1883'],
       ['Collector', 'paho-mqtt + SQLite outbox', 'Kiểm tra hợp lệ, commit trước khi ACK QoS 1'],
       ['Database', 'InfluxDB 2.7', 'Bucket "iot", retention 30 ngày, sensor_raw / sensor_clean'],
       ['Tiền xử lý', 'pandas + numpy', 'IQR, resample 10 s, rolling mean, delta, chuẩn hóa'],
       ['Dashboard', 'Streamlit', 'Hiển thị thô + đã xử lý, tự refresh 5 giây, cổng 8501']],
      widths=[3.0, 4.6, 7.4])

# ===================== 3. THIET BI WOKWI =====================
h('3. Thiết bị nhúng trên Wokwi (firmware)', 13.5)
para('Dự án Wokwi "B23DCAT148 - Bai 2 IoT" (mã 477199664093349889) gồm ESP32 DevKit V1, cảm biến DHT22, '
     'cảm biến siêu âm HC-SR04 và một LED trạng thái. Firmware dùng thư viện PubSubClient và DHTesp: kết nối '
     'Wi-Fi Wokwi-GUEST, kết nối MQTT tới HiveMQ, và mỗi 5 giây đọc nhiệt độ, độ ẩm, khoảng cách rồi publish '
     'một bản tin JSON. LED nháy 100 ms mỗi lần gửi thành công để báo trạng thái.')
table(['Chân ESP32', 'Nối tới', 'Ghi chú'],
      [['GPIO 15', 'DHT22 DATA', 'Nhiệt độ, độ ẩm'],
       ['GPIO 5', 'HC-SR04 TRIG', 'Phát xung kích'],
       ['GPIO 18', 'HC-SR04 ECHO', 'Đọc thời gian phản hồi'],
       ['GPIO 2', 'LED (qua điện trở)', 'Nháy khi publish thành công']],
      widths=[3.0, 4.5, 7.5])
code('const char* MQTT_SERVER = "broker.hivemq.com";   const char* MQTT_TOPIC = "lab2/sensors/esp32_01/data";\n'
     'payload = {"device_id":"esp32_01","temperature":24.00,"humidity":40.00,\n'
     '           "distance_cm":403.49,"rssi":-84,"sequence":7,"uptime_s":39}')
img(os.path.join(EV, 'wokwi_circuit_crop.png'),
    'Hình 2. Sơ đồ mạch firmware trên Wokwi (ESP32, DHT22, HC-SR04, LED).', 4.3)
img(os.path.join(EV, 'wokwi_serial_crop.png'),
    'Hình 3. Serial Monitor của Wokwi khi chạy: thiết bị in ra bản tin [PUBLISH] dạng JSON.', 5.0)

# ===================== 4. THU THAP =====================
h('4. Thu thập dữ liệu IoT (MQTT)', 13.5)
para('Thiết bị publish lên broker công cộng HiveMQ. Vì máy tính không truy cập được broker công cộng theo cách '
     '“localhost”, một client bridge subscribe topic của thiết bị rồi publish lại vào Mosquitto nội bộ theo đúng '
     'định dạng mà collector yêu cầu. Nhờ vậy collector, database và tiền xử lý không cần thay đổi gì.')
code('client.subscribe("lab2/sensors/esp32_01/data")   # từ HiveMQ\n'
     '... publish("iot/lab2/esp32_01/telemetry", normalized_json)   # vào Mosquitto nội bộ')
img(os.path.join(EV, 'fig_hivemq_log.png'),
    'Hình 4. Client local subscribe HiveMQ nhận liên tục bản tin của esp32_01, temperature = 24.00 °C, humidity = 40.00 %, distance ≈ 403 cm.', 5.7)
para('Collector subscribe wildcard iot/lab2/+/telemetry với QoS 1, đối chiếu device_id trong payload với topic để '
     'chống gán sai nguồn và kiểm tra dải giá trị theo bảng sau (validation.py). Bản tin sai bị từ chối và ghi log, '
     'không làm dừng collector.', size=12)
table(['Trường', 'Quy tắc kiểm tra'],
      [['device_id', 'Chuỗi khớp [A-Za-z0-9_-]{1,40} và phải trùng với topic'],
       ['ts_ms / seq', 'Số nguyên ≥ 0; ts_ms không cũ quá 24 giờ, không vượt tương lai quá 60 giây'],
       ['temperature', 'Số hữu hạn trong −40 … 80 °C (được phép thiếu/null)'],
       ['humidity', 'Số hữu hạn trong 0 … 100 % (được phép thiếu/null)'],
       ['Ràng buộc', 'Cho phép một cảm biến thiếu; không chấp nhận thiếu cả hai; payload tối đa 4096 byte']],
      widths=[3.3, 11.7])

# ===================== 5. LUU TRU =====================
h('5. Lưu trữ dữ liệu IoT — schema database', 13.5)
para('Collector không ghi thẳng vào InfluxDB ngay khi nhận bản tin: mỗi bản tin hợp lệ được ghi vào SQLite '
     '(WAL, synchronous=FULL) và chỉ ACK QoS 1 sau khi commit thành công. Nếu InfluxDB tạm hỏng, bản tin vẫn nằm '
     'an toàn trong outbox và writer tự thử lại sau mỗi 3 giây; khóa chống trùng (device_id, ts_ms) khiến ghi lại '
     'là idempotent. Đây là cơ chế bảo toàn dữ liệu khi mất kết nối nhất thời.')
table(['Measurement', 'Tag', 'Timestamp', 'Fields'],
      [['sensor_raw', 'device_id', 'ts_ms (thời gian thiết bị)',
        'temperature, humidity, seq, received_ms, latency_ms'],
       ['sensor_clean', 'device_id', 'Đầu cửa sổ UTC 10 giây',
        'temperature, humidity, *_rolling_mean, *_delta, *_norm (kèm cờ *_valid), sample_count, outlier_count']],
      widths=[2.6, 2.0, 3.2, 7.2])
para('Không dùng seq hay timestamp làm tag vì chúng tăng liên tục gây bùng nổ cardinality. Giá trị thiếu được lưu '
     'placeholder 0.0 kèm cờ *_valid = false để dashboard không nhầm số 0 với số đo thật. Bucket "iot" đặt retention '
     '30 ngày.', size=12)
img(os.path.join(EV2, 'ev3_store.png'),
    'Hình 5. Outbox SQLite đã ghi đủ bản tin và InfluxDB có cả sensor_raw lẫn sensor_clean sau khi tiền xử lý.', 4.6)

# ===================== 6. TIEN XU LY =====================
h('6. Tiền xử lý dữ liệu', 13.5)
para('preprocess.py đọc dữ liệu thô theo khoảng thời gian, xử lý riêng từng thiết bị rồi ghi vào sensor_clean:')
numbered([
    'Sắp xếp theo thời gian, loại bỏ bản ghi trùng timestamp.',
    'Phát hiện bất thường theo IQR: điểm nằm ngoài [Q1−1,5·IQR, Q3+1,5·IQR] bị thay bằng NaN (chỉ áp dụng khi có '
    'tối thiểu 8 giá trị và IQR > 0).',
    'Resampling cửa sổ 10 giây bằng trung bình; đếm sample_count và outlier_count mỗi cửa sổ.',
    'Điền thiếu bằng forward-fill tối đa 2 cửa sổ (20 giây); khoảng thiếu dài hơn giữ NaN, không điền ngược từ tương lai.',
    'Tạo đặc trưng rolling mean 3 cửa sổ (30 giây) và delta so với cửa sổ trước.',
    'Chuẩn hóa min-max theo khoảng vật lý cố định: nhiệt độ (x+40)/120, độ ẩm x/100; chỉ ghi các cửa sổ đã kết thúc.',
])
img(os.path.join(EV2, 'fig_preprocess.png'),
    'Hình 6. Trên: sensor_raw với các điểm bất thường bị IQR đánh dấu. Dưới: sensor_clean sau resample 10 giây — rolling mean làm mượt nhiễu.', 5.6)

# ===================== 7. KET QUA =====================
h('7. Kết quả thực nghiệm (dashboard, bảng số liệu)', 13.5)
para('Dashboard Streamlit đọc cả sensor_raw và sensor_clean, tự cập nhật mỗi 5 giây: hiển thị số bản tin, độ trễ '
     'trung bình và P95 tới collector, khoảng trống seq; bên dưới là biểu đồ dữ liệu thô, dữ liệu đã xử lý và bảng '
     '30 cửa sổ gần nhất. Khi thiết bị Wokwi (esp32_01) chạy, thiết bị này xuất hiện trong danh sách giám sát và '
     'toàn bộ pipeline hoạt động như với thiết bị thật.')
img(os.path.join(EV, 'wokwi_04_dashboard.png'),
    'Hình 7. Dashboard nhận thiết bị esp32_01 từ Wokwi và hiển thị trực tiếp dữ liệu nhiệt độ/độ ẩm.', 4.5)
img(os.path.join(EV, 'fig_raw_clean_wokwi.png'),
    'Hình 8. Dữ liệu esp32_01 (Wokwi) trong InfluxDB: sensor_raw và sensor_clean (DHT22 mô phỏng giữ 24 °C / 40 %, nên hai đường gần như phẳng).', 5.4)
table(['Chỉ số', 'Giá trị đo được'],
      [['Thiết bị', 'esp32_01 (Wokwi ESP32 + DHT22 + HC-SR04) — chu kỳ 5 giây'],
       ['Kênh vận chuyển', 'HiveMQ công cộng → bridge → Mosquitto nội bộ'],
       ['Độ trễ tới collector', 'trung bình 1,5 ms — P95 4,0 ms (đo trên bản tin esp32_01)'],
       ['Nhiệt độ / độ ẩm mô phỏng', '24,00 °C / 40,00 % (giá trị mặc định của DHT22 trong Wokwi)'],
       ['Khoảng cách siêu âm', '≈ 403 cm (ổn định, sai khác < 0,2 cm giữa các mẫu)'],
       ['Pipeline lưu trữ', 'Collector + outbox SQLite + InfluxDB sensor_raw'],
       ['Tiền xử lý', 'resample 10 giây, rolling mean, delta, chuẩn hóa — ghi sensor_clean']],
      widths=[5.0, 10.0])

# ===================== 8. PHAN TICH =====================
h('8. Phân tích độ trễ, vấn đề lưu trữ và đề xuất cải tiến', 13.5)
para('Độ trễ latency_ms = received_ms − ts_ms đo từ lúc collector nhận so với timestamp thiết bị tạo mẫu. Giá trị '
     'trung bình 1,5 ms và P95 4,0 ms rất nhỏ vì bridge, broker và collector chạy cùng một máy; đồng thời bản tin '
     'đi vòng qua HiveMQ công cộng nên độ trễ thực tế phụ thuộc mạng Internet. Đây KHÔNG phải độ trễ end-to-end: '
     'chưa gồm thời gian ghi InfluxDB, tiền xử lý và chu kỳ refresh 5 giây của dashboard.', size=12)
para('Hạn chế: broker công cộng không có xác thực/TLS nên bất kỳ ai cũng đọc và ghi được cùng topic; chu kỳ publish '
     '5 giây của Wokwi khá thưa nên cửa sổ resample 10 giây chỉ có ~2 mẫu; DHT22 mô phỏng trả giá trị không đổi nên '
     'chưa thể hiện được dao động thực tế; retention 30 ngày tự xóa dữ liệu cũ. Đề xuất: (1) dùng topic riêng khó '
     'đoán và bật TLS + xác thực; (2) thay IQR batch bằng MAD/EWMA cuộn thời gian để phát hiện bất thường real-time; '
     '(3) ghi InfluxDB theo lô; (4) tách retention riêng cho sensor_clean; (5) đo riêng độ trễ ghi DB và độ trễ '
     'hiển thị dashboard.', size=12)

# ===================== 9. KHO KHAN =====================
h('9. Khó khăn và cách giải quyết', 13.5)
table(['Khó khăn', 'Cách giải quyết'],
      [['Thiết bị Wokwi publish lên HiveMQ nhưng collector chỉ nghe Mosquitto nội bộ',
        'Viết bridge subscribe HiveMQ rồi publish lại vào Mosquitto theo đúng định dạng collector yêu cầu'],
       ['Topic công cộng bị thiết bị khác ghi trùng',
        'Nhiều bạn dùng chung topic lab2/sensors/esp32_01/data nên lẫn bản tin lạ; lọc theo dấu vân tay thiết bị '
        'và khuyến nghị đặt topic riêng'],
       ['DHT22 trên Wokwi trả giá trị cố định', 'Chấp nhận và ghi rõ là dữ liệu mô phỏng; dùng dữ liệu có chèn bất '
        'thường để minh họa thuật toán tiền xử lý'],
       ['InfluxDB báo 401 Unauthorized', 'Đồng bộ token/org/bucket trong .env với thiết lập lúc khởi tạo DB'],
       ['Bản tin bị từ chối do timestamp', 'Dùng epoch mili-giây; không dùng millis() (uptime) làm timestamp']],
      widths=[5.5, 9.5])

# ===================== 10. KET LUAN =====================
h('10. Kết luận', 13.5)
para('Firmware ESP32 viết trên Wokwi đã chạy đúng: đọc cảm biến, đóng gói JSON và publish lên MQTT thành công, '
     'được minh chứng bằng Serial Monitor và client subscribe nhận dữ liệu thật. Bằng cầu nối HiveMQ → Mosquitto, '
     'dữ liệu từ thiết bị Wokwi chảy trọn vẹn qua pipeline lưu trữ và tiền xử lý rồi hiển thị trên dashboard. '
     'Ba yếu tố cốt lõi được rút ra: tính toàn vẹn dữ liệu (outbox + QoS), thiết kế schema time-series hợp lý '
     '(tag hóa device_id, tránh cardinality cao) và hiểu đúng phạm vi của chỉ số độ trễ. Hạn chế và hướng cải '
     'tiến đã nêu ở mục 8 để triển khai ở phiên bản tiếp theo.')

doc.save(OUT)
print('saved', OUT)
