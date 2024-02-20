from features.configuration.configuration import Configuration
from features.mqtt_clients.base_client import MqttClient
from errors.device_exceptions import DeviceNotRecognized


class TemperatureSensorFactory:

    def __init__(self, config: Configuration, mqtt_client: MqttClient):
        self.config = config
        self.temperature_sensor_config = config.devices.temperature_sensor
        self.client = mqtt_client

    def create(self):
        device_type = self.temperature_sensor_config.type
        if device_type == "dht11":
            pass

        raise DeviceNotRecognized(f"Device type: {device_type} is unknown.")
