from umqtt.simple import MQTTClient
from features.mqtt_clients.base_client import MqttClient
from features.configuration.configuration import Mqtt
from loggers.logger import Logger


class HiveMqMqttClient(MqttClient):
    def __init__(self, base_device_topic: str, config: Mqtt, logger: Logger):
        super().__init__(base_device_topic, config, logger)

        self._subscribed = []

        self._client = MQTTClient(
            client_id=self._config.client_id,
            server=self._config.server,
            port=self._config.port,
            user=self._config.user,
            password=self._config.password,
            keepalive=self._config.keep_alive,
            ssl=True,
            ssl_params={"server_hostname": self._config.server})

        self._client.set_callback(self._callback)

    def subscribe_provided_topics(self):
        for topic in self._callbacks.keys():
            if topic in self._subscribed:
                continue
            formatted_topic = self._format_topic(topic)
            self._client.subscribe(formatted_topic)
            self._logger.log_debug(f"Subscribed to topic: {formatted_topic}")

            self._subscribed.append(topic)

    def connect(self):
        self._logger.log_info(f"Connecting to broker: {self._config.client_id}")
        self._client.connect()
        self.subscribe_provided_topics()
        self._logger.log_info(f"Successfully connected to broker with client_id: {self._config.client_id}")

    def _callback(self, topic, message):
        try:
            topic = topic.decode("utf-8")
            data = message.decode("utf-8")

            if topic not in self._callbacks:
                self._logger.log_warning(f"{topic} not found in topics. Ignoring message")
                return

            function = self._callbacks[topic]
            function(data, self._logger)

        except Exception as e:
            self._logger.log_error(f"Error receiving data on {topic}. Error {e}")
        else:
            self._logger.log_info(f"Data from topic '{topic}' received. ")
            self._logger.log_debug(f"Received Topic: '{topic}' Payload: {data}. ")

    def publish(self, topic, payload):
        payload_bytes = payload.encode('utf-8')
        topic_bytes = topic.encode('utf-8')
        self._client.publish(topic_bytes, payload_bytes)
        self._logger.log_info(f"Published data on topic {topic}")
        self._logger.log_debug(f"Sending Topic: '{topic}' Payload: {payload}. ")
