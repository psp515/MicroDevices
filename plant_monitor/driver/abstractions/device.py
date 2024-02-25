from features.configuration.configuration import Configuration, DeviceConfiguration
from features.mqtt_clients.base_client import MqttClient
from loggers.logger import Logger


class Device:
    def __init__(self,
                 config: Configuration,
                 device_config: DeviceConfiguration,
                 mqtt_client: MqttClient,
                 logger: Logger):
        self.config = config
        self.device_config = device_config
        self.mqtt_client = mqtt_client
        self.logger = logger
        self.push_next = False

    @property
    def id(self):
        return self.device_config.id

    @property
    def update_config_topic(self):
        return self.device_config.update_topic

    def update_config(self, data):
        pass

    def get_subscriptions(self):
        return []

    def push_newest_data(self):
        self.push_next = True

    def loop(self):
        pass
