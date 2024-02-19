from loggers.logger import Logger
from features.configuration.configuration import Mqtt


class MqttClient:
    def __init__(self, base_device_topic: str, config: Mqtt, logger: Logger):
        self._logger = logger
        self._config = config
        self._callbacks = {}
        self._client = None
        self._base_topic = base_device_topic

    def _format_topic(self, topic: str):
        return f"{self._base_topic}{topic}"

    def _callback(self, topic, message):
        self._logger.log_info(f"Fake callback from MQTT Broker.")

    def update(self):
        self._client.check_msg()

    def connect(self):
        self._logger.log_info(f"Fake connect to MQTT Broker.")

    def publish(self, topic: str, json_data: str):
        self._logger.log_info(f"Fake publish on topic: {topic} data: {json_data}")

    def subscribe(self, topic: str, callback):
        self._logger.log_info(f"Subscribed to topic: {topic}")
        self._callbacks[topic] = callback
