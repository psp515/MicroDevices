from features.clients.hivemq_client import HiveMqMqttClient


class MqttFactory:
    def __init__(self, config):
        self.config = config

    def create(self):
        pass