"""
A simple example that connects to the Adafruit IO MQTT server
and publishes values that represent a sine wave
"""

import network
import time
from math import sin
from simple import MQTTClient
from machine import Pin
import utime

trigger = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)
def ultra():
   trigger.low()
   utime.sleep_us(2)
   trigger.high()
   utime.sleep_us(5)
   trigger.low()
   while echo.value() == 0:
       signaloff = utime.ticks_us()
   while echo.value() == 1:
       signalon = utime.ticks_us()
   timepassed = signalon - signaloff
   distance = (timepassed * 0.0343) / 2
   print(distance," cm")
   return distance

# Fill in your WiFi network name (ssid) and password here:
wifi_ssid = "Inteli-welcome"
wifi_password = ""

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

# Fill in your Adafruit IO Authentication and Feed MQTT Topic details
mqtt_host = "industrial.api.ubidots.com"
mqtt_username = "BBUS-3TxBOYXyy5rqMAx2Y0uYOSTVW5gq8L"  # Your Adafruit IO username
mqtt_password = ""  # Adafruit IO Key
mqtt_publish_topic = "/v1.6/devices/demo/var"  # The MQTT topic for your Adafruit IO Feed

# Enter a random ID for this MQTT Client
# It needs to be globally unique across all of Adafruit IO.
mqtt_client_id = "somethingreallyrandomandunique123"

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client.connect()

# Publish a data point to the Adafruit IO MQTT server every 3 seconds
# Note: Adafruit IO has rate limits in place, every 3 seconds is frequent
#  enough to see data in realtime without exceeding the rate limit.
counter = 0
try:
    while True:
        # Generate some dummy data that changes every loop
        sine = ultra()
        
        # Publish the data to the topic!
        print(f'Publish {sine:.2f}')
        mqtt_client.publish(mqtt_publish_topic, str(sine))
        
        # Delay a bit to avoid hitting the rate limit
        time.sleep(3)
except Exception as e:
    print(f'Failed to publish message: {e}')
finally:
    mqtt_client.disconnect()