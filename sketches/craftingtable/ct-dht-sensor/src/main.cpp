#include <Arduino.h>
#include <DHT.h>

// Pin assignments — must match wiring.yaml
constexpr int DHT_PIN = 7;

// Sensor type: DHT11 (blue) or DHT22 (white)
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(9600);
  Serial.println("DHT11 Temperature & Humidity Sensor");
  dht.begin();
}

void loop() {
  delay(2000);  // DHT11 needs at least 2 seconds between reads

  float humidity    = dht.readHumidity();
  float tempC       = dht.readTemperature();
  float tempF       = dht.readTemperature(true);

  if (isnan(humidity) || isnan(tempC) || isnan(tempF)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  float heatIndexC = dht.computeHeatIndex(tempC, humidity, false);
  float heatIndexF = dht.computeHeatIndex(tempF, humidity);

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print("%  Temp: ");
  Serial.print(tempC);
  Serial.print("C ");
  Serial.print(tempF);
  Serial.print("F  Heat index: ");
  Serial.print(heatIndexC);
  Serial.print("C ");
  Serial.print(heatIndexF);
  Serial.println("F");
}
