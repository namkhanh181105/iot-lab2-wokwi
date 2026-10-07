#include <WiFi.h>
#include <PubSubClient.h>
#include <DHTesp.h>

// 1. Cáº¥u hÃ¬nh Wi-Fi Wokwi
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";

// 2. Cáº¥u hÃ¬nh MQTT Broker (HiveMQ cÃ´ng cá»ng) & Topic phÃ¢n cáº¥p
const char* MQTT_SERVER = "broker.hivemq.com";
const int MQTT_PORT = 1883;
const char* MQTT_TOPIC = "lab2/sensors/esp32_01/data";
const char* DEVICE_ID = "esp32_01";

// 3. Khai bÃ¡o chÃ¢n GPIO giá»¯ nguyÃªn tá»« BÃ i 1
const int DHT_PIN = 15;     // DHT22 DATA -> GPIO 15
const int TRIG_PIN = 5;     // HC-SR04 TRIG -> GPIO 5
const int ECHO_PIN = 18;    // HC-SR04 ECHO -> GPIO 18
const int LED_PIN = 2;      // LED tráº¡ng thÃ¡i -> GPIO 2

const unsigned long SEND_INTERVAL_MS = 5000; // Chu ká»³ gá»­i 5 giÃ¢y

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
DHTesp dht;

unsigned long lastSend = 0;
unsigned long sequenceNo = 0;

void connectWiFi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD, 6);
  Serial.print("Connecting WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
}

void connectMQTT() {
  while (!mqttClient.connected()) {
    // Client ID ngáº«u nhiÃªn Äá» trÃ¡nh xung Äá»t káº¿t ná»i
    String clientId = "ESP32-Lab2-" + String((uint32_t)ESP.getEfuseMac(), HEX);
    Serial.print("Connecting MQTT...");
    if (mqttClient.connect(clientId.c_str())) {
      Serial.println(" connected to HiveMQ!");
    } else {
      Serial.printf(" failed, rc=%d. Retry in 2s\n", mqttClient.state());
      delay(2000);
    }
  }
}

float readDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH);
  return (float)(duration * 0.0343 / 2.0);
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  dht.setup(DHT_PIN, DHTesp::DHT22);
  connectWiFi();
  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) connectWiFi();
  if (!mqttClient.connected()) connectMQTT();
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastSend >= SEND_INTERVAL_MS) {
    lastSend = now;

    TempAndHumidity data = dht.getTempAndHumidity();
    float temp = data.temperature;
    float hum = data.humidity;
    float distance = readDistance();

    // Kiá»m tra dá»¯ liá»u há»£p lá» trÆ°á»c khi gá»­i
    if (!isnan(temp) && !isnan(hum) && isfinite(temp) && isfinite(hum)) {
      sequenceNo++;
      long rssi = WiFi.RSSI();
      unsigned long uptime_s = now / 1000;

      // ÄÃ³ng gÃ³i JSON Payload chuáº©n cho BÃ i 2
      String payload = "{";
      payload += "\"device_id\":\"" + String(DEVICE_ID) + "\",";
      payload += "\"temperature\":" + String(temp, 2) + ",";
      payload += "\"humidity\":" + String(hum, 2) + ",";
      payload += "\"distance_cm\":" + String(distance, 2) + ",";
      payload += "\"rssi\":" + String(rssi) + ",";
      payload += "\"sequence\":" + String(sequenceNo) + ",";
      payload += "\"uptime_s\":" + String(uptime_s);
      payload += "}";

      if (mqttClient.publish(MQTT_TOPIC, payload.c_str())) {
        Serial.print("[PUBLISH]: ");
        Serial.println(payload);
        digitalWrite(LED_PIN, HIGH);
        delay(100);
        digitalWrite(LED_PIN, LOW);
      } else {
        Serial.println("Publish failed");
      }
    } else {
      Serial.println("Lá»i Äá»c dá»¯ liá»u cáº£m biáº¿n DHT22!");
    }
  }
}