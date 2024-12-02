import machine
from machine import Pin
import esp
import esp32
import time
import network
import webrepl
import gc

# local libraries
import secrets
import mcuconfig as config
from mcuperipherals import MCUSensor, MCUAction
from umqttsimple import MQTTClient

esp.osdebug(None)
gc.collect()

# constants
DEVICE_NAME = config.DEVICE_NAME

# libraries
wifi = network.WLAN(network.STA_IF)
mqtt = MQTTClient(DEVICE_NAME, secrets.MQTT_BROKER_IP, user=secrets.MQTT_USER, password=secrets.MQTT_PASSWORD)

# boot logic
print('\nBooting device %s...' % (DEVICE_NAME), end="\n\n")

def setup_wifi(ssid, pwd):
    if not wifi.isconnected():
        wifi.ipconfig(addr4=config.STATIC_IP4_CIDR)
        wifi.active(True)
        wifi.connect(ssid, pwd)
        print('Wifi connecting to network...')
        while not wifi.isconnected():
            pass
    print('Wifi network connected:', wifi.ifconfig(), end="\n\n")
setup_wifi(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)

mqtt_connected = mqtt.safe_connect()
print('\n%s to %s MQTT broker' % ('Connected' if mqtt_connected else 'FAILED connecting', mqtt.server))

if config.ENABLE_WEB_REPL:
    webrepl.start(password=secrets.WEB_REPL_PASSWORD)

print('\nBooting %s complete' % (DEVICE_NAME), end="\n\n")
