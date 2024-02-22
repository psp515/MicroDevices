import ujson

from abstractions.device import Device
from features.configuration.configuration import Configuration, TemperatureDeviceConfiguration
from features.mqtt_clients.base_client import MqttClient
from loggers.logger import Logger
import machine
import dht
from utime import ticks_ms, ticks_diff


class DHT11(Device):

    DHT_READ_SPAN = 2000

    def __init__(self,
                 config: Configuration,
                 device_config: TemperatureDeviceConfiguration,
                 mqtt_client: MqttClient,
                 logger: Logger):
        super().__init__(config, device_config, mqtt_client, logger)
        dht_pin = machine.Pin(device_config.data_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.device_config = device_config
        self._sensor = dht.DHT11(dht_pin)
        self._humidity = None
        self._temp = None
        self._last_read = ticks_ms()

    def loop(self):
        try:
            current_time = ticks_ms()
            if abs(ticks_diff(current_time, self._last_read)) < DHT11.DHT_READ_SPAN:
                return

            self._last_read = current_time

            self.logger.log_info("Starting loop of dht11 sensor.")
            self._sensor.measure()
            temp = self._sensor.temperature()
            humidity = self._sensor.humidity()

            self.logger.log_debug(f"Measured temp: {temp}, hum: {humidity}.")

            if self.push_next or self._should_update_temp(temp) or self._should_update_humidity(humidity):
                self.logger.log_debug(f"Updating dht11 data.")
                payload = self._create_payload(temp, humidity)
                topic = self.device_config.update_topic
                self.logger.log_debug(f"Topic: {topic} Payload: {payload}")
                self.mqtt_client.publish(topic, payload)
                self.push_next = False

        except BaseException as e:
            self.logger.log_debug(f"Exception in dht11 temperature sensor loop: {e}")
            self.logger.log_error(f"Dht11 sensor with id {self.id} unexpectedly failed.")

    def _should_update_humidity(self, humidity):
        if self._humidity is None:
            self._humidity = humidity
            return True

        if self.device_config.hum_threshold.type == "percent":
            if abs(self._humidity - humidity) > self.device_config.hum_threshold.value:
                self._humidity = humidity
                return True

        return False

    def _should_update_temp(self, temp):
        if self._temp is None:
            self._temp = temp
            return True

        if self.device_config.temp_threshold.type == "degrees":
            if abs(self._temp - temp) > self.device_config.temp_threshold.value:
                self._temp = temp
                return True

        return False

    def _create_payload(self, temp, humidity):
        temp_unit = self.device_config.temp_threshold.unit
        self.logger.log_debug(f"DHT11 temp unit: {temp_unit}")

        if temp_unit == "F":
            temp = self.celsius_to_fahrenheit(temp)
        elif temp_unit == "K":
            temp = self.celsius_to_kelvin(temp)

        self.logger.log_debug(f"Updated temp: {temp}")

        data = {
            "device": self.device_config.id,
            "temperature": {
                "value": temp,
                "unit": temp_unit
            },
            "humidity": {
                "value": humidity,
                "unit": self.device_config.hum_threshold.unit
            }
        }

        self.logger.log_debug(f"Formatted payload: {data}")

        return ujson.dumps(data)

    @staticmethod
    def celsius_to_fahrenheit(celsius):
        fahrenheit = (celsius * 9 / 5) + 32
        return fahrenheit

    @staticmethod
    def celsius_to_kelvin(celsius):
        kelvin = celsius + 273.15
        return kelvin
