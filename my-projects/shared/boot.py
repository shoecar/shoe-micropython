# generic python modules
import time
import gc
# Micropython modules
import esp
import network
import webrepl
from machine import Pin, Timer, reset
# local modules
import secrets
import mcuconfig as config
from umqttsimple import MQTTClient

# constants
DEVICE_NAME = config.DEVICE_NAME
# ESP32 board settings:
#  XIAO_ESP32C3 - https://files.seeedstudio.com/wiki/XIAO_WiFi/pin_map-2.png
BUTTON_PIN = Pin(6, Pin.IN, Pin.PULL_UP)

# libraries
wifi = network.WLAN(network.STA_IF)
mqtt = MQTTClient(DEVICE_NAME, secrets.MQTT_BROKER_IP, user=secrets.MQTT_USER, password=secrets.MQTT_PASSWORD)

# setup helpers
def setup_wifi():
    if not wifi.isconnected():
        wifi.ipconfig(addr4=config.STATIC_IP4_CIDR)
        wifi.active(True)
        wifi.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
        print('WIFI connecting to network:', secrets.WIFI_SSID, end='')
        while not wifi.isconnected():
            print('.', end='')
            time.sleep_ms(333)
            pass
    print('\nWIFI network connected:', wifi.ifconfig())

def setup_mqtt():
    mqtt_connected = mqtt.safe_connect()
    print('\n%s to %s MQTT broker' % ('Connected' if mqtt_connected else 'FAILED connecting', mqtt.server))

def close_webrepl(timer):
    webrepl.stop()
    print('WebREPL closed after running for %s minutes' % config.WEB_REPL_CLOSE_AFTER_MINUTES)

def setup_webrepl():
    if config.ENABLE_WEB_REPL:
        print('\nWebREPL Enabled: ', end='')
        webrepl.start(password=secrets.WEB_REPL_PASSWORD)

        if config.WEB_REPL_CLOSE_AFTER_MINUTES:
            close_timer = Timer(0)
            close_delay_ms = config.WEB_REPL_CLOSE_AFTER_MINUTES * 60 * 1000
            close_timer.init(period=close_delay_ms, mode=Timer.ONE_SHOT, callback=close_webrepl)
            print('Timer set to close WebREPL in %s minutes' % config.WEB_REPL_CLOSE_AFTER_MINUTES)

# boot logic
def boot():
    print('\nBooting device %s...' % DEVICE_NAME, end='\n\n')

    esp.osdebug(None)
    gc.collect()

    setup_wifi()
    setup_mqtt()
    setup_webrepl()

    print('\nBooting %s complete' % DEVICE_NAME, end='\n\n')

boot()
