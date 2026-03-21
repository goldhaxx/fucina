#include <Arduino.h>
#include <WiFi.h>

// Pin assignments — must match wiring.yaml
// GPIO 2 is safe for general use on ESP32
constexpr int LED_PIN = 2;

// WiFi Access Point credentials
const char* AP_SSID     = "HomeLights";
const char* AP_PASSWORD = "";  // Open network (no password)

WiFiServer server(80);

// HTML page with on/off buttons
const char HTML_PAGE[] = R"rawliteral(
<!DOCTYPE HTML>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  body { font-family: sans-serif; text-align: center; margin-top: 40px; }
  .button { font-size: 40px; padding: 20px 48px; margin: 10px; }
</style>
</head>
<body>
<h1>Light Control</h1>
<p><a href="/H"><button class="button">Turn On</button></a></p>
<p><a href="/L"><button class="button">Turn Off</button></a></p>
</body>
</html>
)rawliteral";

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  Serial.println();
  Serial.println("Configuring WiFi access point...");

  if (!WiFi.softAP(AP_SSID, AP_PASSWORD)) {
    Serial.println("AP creation failed!");
    while (true);
  }

  IPAddress ip = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(ip);
  server.begin();
  Serial.println("Web server started — connect to WiFi 'HomeLights'");
  Serial.print("Then browse to http://");
  Serial.println(ip);
}

void loop() {
  WiFiClient client = server.available();
  if (!client) return;

  Serial.println("New client connected");
  String currentLine = "";

  while (client.connected()) {
    if (!client.available()) continue;

    char c = client.read();
    Serial.write(c);

    if (c == '\n') {
      if (currentLine.length() == 0) {
        // End of HTTP headers — send response
        client.println("HTTP/1.1 200 OK");
        client.println("Content-type:text/html");
        client.println();
        client.println(HTML_PAGE);
        client.println();
        break;
      } else {
        currentLine = "";
      }
    } else if (c != '\r') {
      currentLine += c;
    }

    if (currentLine.endsWith("GET /H")) {
      digitalWrite(LED_PIN, HIGH);
    }
    if (currentLine.endsWith("GET /L")) {
      digitalWrite(LED_PIN, LOW);
    }
  }

  client.stop();
  Serial.println("Client disconnected");
}
