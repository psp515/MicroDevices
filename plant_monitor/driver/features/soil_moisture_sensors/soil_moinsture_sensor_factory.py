from features.configuration.configuration import Configuration, DeviceConfiguration
from features.soil_moisture_sensors.analog_soil_moisture import AnalogSoilMoistureSensor
from features.soil_moisture_sensors.digital_soil_moisture import DigitalSoilMoistureSensor
from features.mqtt_clients.base_client import MqttClient
from errors.device_exceptions import DeviceNotRecognized
from loggers.logger import Logger


class SoilMoistureSensorFactory:

    def __init__(self,
                 config: Configuration,
                 device_config: DeviceConfiguration,
                 mqtt_client: MqttClient,
                 logger: Logger):
        self.config = config
        self.device_config = device_config
        self.client = mqtt_client
        self.logger = logger

    def create(self):
        device_type = self.device_config.type

        if device_type == "analog":
            return AnalogSoilMoistureSensor(self.config, self.device_config, self.client, self.logger)

        if device_type == "digital":
            return DigitalSoilMoistureSensor(self.config, self.device_config, self.client, self.logger)

        raise DeviceNotRecognized(f"Device type: {device_type} is unknown.")
