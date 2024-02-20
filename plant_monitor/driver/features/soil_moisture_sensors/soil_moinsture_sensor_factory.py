from features.configuration.configuration import Configuration, DeviceConfiguration
from features.mqtt_clients.base_client import MqttClient
from errors.device_exceptions import DeviceNotRecognized


class SoilMoistureSensorFactory:

    def __init__(self, config: Configuration, device_config: DeviceConfiguration, mqtt_client: MqttClient):
        self.config = config
        self.device_config = device_config
        self.client = mqtt_client

    def create(self):
        device_type = self.device_config.type

        if device_type == "analog":
            pass

        if device_type == "digital":
            pass

        raise DeviceNotRecognized(f"Device type: {device_type} is unknown.")
