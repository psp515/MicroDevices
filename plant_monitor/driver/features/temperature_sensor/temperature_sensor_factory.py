from features.configuration.configuration import Configuration
from features.mqtt_clients.base_client import MqttClient
from errors.device_exceptions import DeviceNotRecognized
from features.temperature_sensor.dht11 import DHT11
from loggers.logger import Logger


class TemperatureSensorFactory:

    def __init__(self, config: Configuration, mqtt_client: MqttClient, logger: Logger):
        self.config = config
        self.temperature_sensor_config = config.devices.temperature_sensor
        self.client = mqtt_client
        self.logger = logger

    def create(self):
        device_type = self.temperature_sensor_config.type
        if device_type == "dht11":
            return DHT11(self.config, self.temperature_sensor_config, self.client, self.logger)

        raise DeviceNotRecognized(f"Device type: {device_type} is unknown.")
