import ujson

from abstractions.device import Device
from features.configuration.configuration import Configuration, TemperatureDeviceConfiguration
from features.mqtt_clients.base_client import MqttClient
from loggers.logger import Logger
import machine
import dht
import time


class DHT11(Device):

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

    def loop(self):
        try:
            self._sensor.measure()
            temp = self._sensor.temperature()
            humidity = self._sensor.humidity()

            if self.push_next or self._should_update_temp(temp) or self._should_update_humidity(humidity):
                payload = self._create_payload(temp, humidity)
                self.client.publish(self.update_config_topic, payload)
                self.push_next = False

        except BaseException as e:
            self.logger.log_debug(f"Exception in dht11 temperature sensor loop: {e}")
            self.logger.log_error(f"Dht11 sensor with id {self.id} unexpectedly failed.")

    def _should_update_humidity(self, humidity):
        if self.device_config.hum_threshold.type == "percent":
            if abs(self._humidity - humidity) > self.device_config.hum_threshold.value:
                self._humidity = humidity
                return True

        return False

    def _should_update_temp(self, temp):
        if self.device_config.temp_threshold.type == "degrees":
            if abs(self._temp - temp) > self.device_config.temp_threshold.value:
                self._temp = temp
                return True

        return False

    def _create_payload(self, temp, humidity):
        temp_unit = self.device_config.temp_threshold.unit

        if temp_unit == "F":
            temp = self.celsius_to_fahrenheit(temp)
        elif temp_unit == "K":
            temp = self.celsius_to_kelvin(temp)

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

        return ujson.dumps(data)

    @staticmethod
    def celsius_to_fahrenheit(celsius):
        fahrenheit = (celsius * 9 / 5) + 32
        return fahrenheit

    @staticmethod
    def celsius_to_kelvin(celsius):
        kelvin = celsius + 273.15
        return kelvin
