global DEVICE_NAME, BUTTON_PIN, mqtt

# ESP32 board settings:
#  XIAO_ESP32C3 - https://files.seeedstudio.com/wiki/XIAO_WiFi/pin_map-2.png
BUTTON_PIN = Pin(6, Pin.IN, Pin.PULL_UP)

BUTTON_PRESSED_TOPIC = '{}/out/button_pressed'.format(DEVICE_NAME)

def mqtt_publish(topic, message, retain=False, qos=0):
  mqtt.publish(str(topic), str(message), retain, qos)
  print('MQTT published\n\t%s: %s' % (topic, message))

# setup
SENSORS = [
  MCUSensor(
    lambda cv: BUTTON_PIN.value() == 0,
    initial_value=False,
    publish_interval_s=2,
    mqtt_topic=BUTTON_PRESSED_TOPIC,
    mqtt_publish_if_values=[True],
    mqtt_publish_cb=mqtt_publish,
  ),
]

try:
  # loop
  while True:
    time.sleep(0.1)

    for sensor in SENSORS:
      sensor.read()
except Exception as e:
  print('Main loop encountered error:', repr(e))
  machine.reset()
