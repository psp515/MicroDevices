from features.configuration.configuration import Configuration, DeviceConfiguration
from features.mqtt_clients.base_client import MqttClient


class Device:
    def __init__(self, config: Configuration, device_config: DeviceConfiguration, mqtt_client: MqttClient):
        self.config = config
        self.device_config = device_config
        self.mqtt_client = mqtt_client

    @property
    def id(self):
        return self.device_config.id

    def loop(self):
        pass
