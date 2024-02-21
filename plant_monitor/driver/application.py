import _thread
from features.configuration.configuration import Configuration
from features.network_connection.wifi_connector import WiFiConnection
from features.mqtt_clients.base_client import MqttClient
from loggers.logger import Logger

from utime import sleep, sleep_ms


class App:
    def __init__(self, devices: [],
                 config: Configuration,
                 connection: WiFiConnection,
                 mqtt: MqttClient,
                 logger: Logger):
        self.devices = devices
        self.configuration = config
        self.connection = connection
        self.mqtt = mqtt
        self._logger = logger

    def start(self):
        self._logger.log_debug("Starting device loop.")
        _thread.start_new_thread(self._device_loop, ())
        self._logger.log_debug("Starting data loop.")
        self._data_loop()

    def _data_loop(self):
        while True:
            if self.connection.is_connected():
                self.mqtt.update()
                sleep_ms(100)
            else:
                self._logger.log_warning("Device disconnected from internet.")
                sleep(1)

    def _device_loop(self):
        while True:
            self._logger.log_debug("Starting device iterations.")
            for device in self.devices:
                device.loop()
            self._logger.log_debug("Finished device iterations.")
            sleep_ms(1000)
