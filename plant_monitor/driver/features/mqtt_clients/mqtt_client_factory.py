from errors.mqtt_clients_errors import InvalidMqttProviderException
from features.mqtt_clients.hivemq_client import HiveMqMqttClient
from features.configuration.configuration import Mqtt
from loggers.logger import Logger


class MqttClientFactory:
    def __init__(self, config: Mqtt, logger: Logger):
        self.config = config
        self.logger = logger

    def create(self):
        if self.config.type == "HiveMq":
            return HiveMqMqttClient(self.config, self.logger)

        raise InvalidMqttProviderException(f"Provider not available: {self.config.type}")
