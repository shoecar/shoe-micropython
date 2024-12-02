import time

class MCUSensor:
  def __init__(
    self,
    read_cb,
    initial_value=None,
    read_interval_s=None,
    publish_interval_s=None,
    mqtt_topic=None,
    mqtt_publish_cb=None,
    mqtt_publish_if_values=[],
  ):
    self.read_cb = read_cb
    self.value = initial_value

    self.read_interval_s = read_interval_s
    self.last_read_at_s = 0

    self.publish_interval_s = publish_interval_s
    self.last_publish_at_s = 0

    self.mqtt_topic = mqtt_topic
    self.mqtt_publish_cb = mqtt_publish_cb
    self.mqtt_publish_if_values = mqtt_publish_if_values

    assert self.mqtt_topic == self.mqtt_publish_cb or self.mqtt_topic and self.mqtt_publish_cb, "Must set mqtt_topic AND mqtt_publish_cb"

  def read(self):
    runtime_s = int(time.time())

    if self.value and self.read_interval_s:
      if (runtime_s - self.last_read_at_s) < self.read_interval_s:
        return
      self.last_read_at_s = runtime_s

    if self.publish_interval_s and (runtime_s - self.last_publish_at_s) < self.publish_interval_s:
      return

    new_value = self.read_cb(self.value)
    if new_value != self.value:
      self.value = new_value
      if self.mqtt_topic and (not self.mqtt_publish_if_values or new_value in self.mqtt_publish_if_values):
        self.last_publish_at_s = runtime_s
        self.mqtt_publish_cb(self.mqtt_topic, str(new_value))
