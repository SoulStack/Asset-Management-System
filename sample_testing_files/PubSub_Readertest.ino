#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define LedPin D0
#define buzPin D0

const char* ssid = "SOUL-IOT";
const char* password = "O2TC*cwt";

const char* mqtt_server = "13.76.182.251";

WiFiClient espClient;
PubSubClient client(espClient);

long now = millis();
long lastMeasure = 0;

void config_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}




void setup() {
  pinMode(buzPin, OUTPUT);
 
  Serial.begin(115200);
  config_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

}

// For this project, you don't need to change anything in the loop function. Basically it ensures that you ESP is connected to your broker
void loop() {

  if (!client.connected()) {
    reconnect();
  }
  if(!client.loop())
    client.connect("ESP8266Client");

  now = millis();
 
 
} 

void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
 
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  if(topic=="reader/dataTx"){
      Serial.print("Changing Room buzzer to ");
      if(messageTemp == "1"){
        digitalWrite(buzPin, 1);
        Serial.print("On");
      }
      else if(messageTemp == "0"){
        digitalWrite(buzPin, 0);
        Serial.print("Off");
      }
  }
  Serial.println();
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    /*CHANGE IF connecting MQTT MULTIPLE CONNECTIONS
     To change the ESP device ID, will have to give a new name to the ESP8266.  */
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");  
      client.subscribe("reader/dataTx");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
