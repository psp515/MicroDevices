from features.configuration.configuration import WiFi
from loggers.logger import Logger
from utime import sleep

import network


class WiFiConnection:

    def __init__(self, wifi_connection: WiFi, logger: Logger):
        self._ssid = wifi_connection.ssid
        self._password = wifi_connection.password
        self._logger = logger
        self._wlan = network.WLAN(network.STA_IF)

    def is_connected(self):
        return self._wlan.isconnected()

    def connect(self):
        self._wlan.active(True)
        self._logger.log_debug(f"Ssid: {self._ssid}, Password: {self._password}")
        self._wlan.connect(self._ssid, self._password)

        sleep(1)
        i = 0
        while not self._wlan.isconnected() and i < 15:
            status = self._wlan.status()
            message = f"Not Connected. Status: {status}, means {self.get_status_description(status)}"
            self._logger.log_warning(message)
            i += 1
            sleep(1)

        status = self._wlan.status()

        if not self._wlan.isconnected():
            status_description = self.get_status_description(status)
            message = f"Not Connected. Status: {status}, means {status_description}."
            self._logger.log_warning(message)
            return False

        status_description = self.get_status_description(status)
        message = f"Connected. Status: {status}, means {status_description}."
        self._logger.log_info(message)
        return True

    @staticmethod
    def get_status_description(status):
        if status == network.STAT_IDLE:
            return "No connection and no activity"
        elif status == network.STAT_CONNECTING:
            return "Connecting in progress"
        elif status == network.STAT_WRONG_PASSWORD:
            return "Failed due to incorrect password"
        elif status == network.STAT_NO_AP_FOUND:
            return "Failed because no access point replied"
        elif status == network.STAT_CONNECT_FAIL:
            return "Failed due to other problems"
        elif status == network.STAT_GOT_IP:
            return "Connection successful"
        return "Unknown"

