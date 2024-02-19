from errors.mqtt_clients_errors import InvalidMqttProviderException
from features.mqtt_clients.hivemq_client import HiveMqMqttClient
from features.mqtt_clients.base_client import MqttClient
from features.configuration.configuration import Configuration
from loggers.logger import Logger


class MqttClientFactory:
    def __init__(self, config: Configuration, logger: Logger):
        self.config = config
        self.logger = logger

    def create(self) -> MqttClient:
        mqtt_config = self.config.connection.mqtt
        base_topic = self.config.base_device_topic

        if mqtt_config.type == "HiveMq":
            return HiveMqMqttClient(base_topic, mqtt_config, self.logger)

        raise InvalidMqttProviderException(f"Provider not available: {mqtt_config.type}")
