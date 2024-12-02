global DEVICE_NAME, mqtt

# ESP32 board settings:
#  XIAO_ESP32C3 - https://files.seeedstudio.com/wiki/XIAO_WiFi/pin_map-2.png
BUTTON_PIN = Pin(6, Pin.IN, Pin.PULL_UP)

def str_runtime(seconds):
  total_hours = int(seconds) // 3600
  secs_remaining = int(seconds) % 3600
  return f'{total_hours // 24}d {total_hours % 24:02}:{secs_remaining // 60:02}:{secs_remaining % 60:02}'

def prnt(*args, **kwargs):
  # print(f'[{str_runtime(time.time())}]', *args, **kwargs)
  print(f'[{int(time.time())}]', *args, **kwargs)

def esp32_reset(*args):
  prnt('\nESP32 Reset initiating...\n')
  machine.reset()

BUTTON_PRESSED_TOPIC = '{}/out/button_pressed'.format(DEVICE_NAME)
ESP32_TEMP_TOPIC = '{}/out/esp32_temp'.format(NAME)
MQTT_PUBLISH_TOPICS = [BUTTON_PRESSED_TOPIC, ESP32_TEMP_TOPIC]
MQTT_SUBSCRIBE_TOPICS = {
    '{}/in/esp32_reset'.format(DEVICE_NAME): esp32_reset,
}

def mqtt_callback(topic, message):
  prnt('MQTT message arrived\n\t%s: %s' % (topic, message))

  subscriber_callback = MQTT_SUBSCRIBE_TOPICS[topic]
  if not subscriber_callback:
    prnt('\tNo callback configured for topic: ', topic)
    return
  else:
    prnt('\tRunning callback "%s" with argument: %s' % (subscriber_callback.__name__, message))
    subscriber_callback(message)

def mqtt_subscribe(subscribe_topics, publish_topics):
  mqtt.set_callback(mqtt_callback)

  for topic_sub in subscribe_topics.keys():
    mqtt.subscribe(topic_sub)

  prnt('MQTT subscriptions to %s setup\n\tSubscribed topics: %s\n\tPublish topics: %s\n' % (mqtt.server, ', '.join(subscribe_topics.keys()), ', '.join(publish_topics)))

def mqtt_publish(topic, message, retain=False, qos=0):
  mqtt.publish(str(topic), str(message), retain, qos)
  prnt('MQTT published\n\t%s: %s' % (topic, message))

# setup
SENSORS = [
  MCUSensor(
    lambda cv: BUTTON_PIN.value() == 0,
    initial_value=False,
    publish_interval_s=2,
    mqtt_topic=BUTTON_PRESSED_TOPIC,
    mqtt_publish_values=[True],
    mqtt_publish_cb=mqtt_publish,
  ),
  MCUSensor(
    lambda cv: esp32.mcu_temperature(),
    read_interval_s=60,
    mqtt_topic=ESP32_TEMP_TOPIC,
    mqtt_publish_cb=mqtt_publish,
  ),
]

MAX_ATTEMPTS = 5
for i in range(MAX_ATTEMPTS):
  try:
    mqtt_subscribe(MQTT_SUBSCRIBE_TOPICS, MQTT_PUBLISH_TOPICS)
    break
  except OSError as e:
    attempt = i + 1
    prnt('MQTT setup encountered error (attempt %s/%s): %s' % (attempt, MAX_ATTEMPTS, e))
    time.sleep(2)
    if (attempt == MAX_ATTEMPTS):
      prnt('MQTT setup failure reached max attempts, reseting ESP32')
      esp32_reset()

# loop
while True:
  time.sleep(0.1)

  try:
    mqtt.check_msg()

    for sensor in SENSORS:
      sensor.read()
  except Exception as e:
    prnt('Main loop encountered error:', repr(e))