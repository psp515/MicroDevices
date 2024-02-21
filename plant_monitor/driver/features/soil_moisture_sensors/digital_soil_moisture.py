from abstractions.device import Device
from abstractions.device import Device
from features.configuration.configuration import Configuration, DeviceConfiguration
from features.mqtt_clients.base_client import MqttClient
from loggers.logger import Logger
import machine


class DigitalSoilMoistureSensor(Device):
    def __init__(self, config: Configuration,
                 device_config: DeviceConfiguration,
                 mqtt_client: MqttClient,
                 logger: Logger):
        super().__init__(config, device_config, mqtt_client, logger)

    def loop(self):
        pass