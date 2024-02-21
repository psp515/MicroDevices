from machine import reset
from loggers.logger_factory import LoggerFactory
from features.configuration.configuration import Configuration
from features.network_connection.wifi_connector import WiFiConnection
from features.mqtt_clients.mqtt_client_factory import MqttClientFactory
from features.temperature_sensor.temperature_sensor_factory import TemperatureSensorFactory
from features.soil_moisture_sensors.soil_moinsture_sensor_factory import SoilMoistureSensorFactory
from application import App

import gc
import ujson
import sys
import globals


def setup_fail(message: str, error_code: int):
    logger.log_error(message)
    if config.mode == globals.DEBUG:
        sys.exit(error_code)
    reset()


if __name__ == '__main__':
    gc.collect()

    logger = LoggerFactory.default_logger()
    config = None
    mqtt_client = None
    devices = []
    app = None

    logger.log_info("Starting parsing configuration.")

    try:
        with open('device_settings.json', 'r') as file:
            json_file = file.read()

        config_data = ujson.loads(json_file)
        # TODO: Add validation to configuration
        config = Configuration(config_data)

        logger.log_info("Finished parsing configuration. Updating logger.")
        # TODO: Update Logger
    except Exception as e:
        logger.log_error(f"Invalid configuration. Please fix configuration. Exception: {str(e)}")
        sys.exit(1)

    connection = WiFiConnection(config.connection.wifi, logger)
    result = connection.connect()

    if not result:
        setup_fail(f"Failed to connect with ssid: {config.connection.wifi.ssid}.", 2)

    try:
        mqtt_client = MqttClientFactory(config, logger).create()
        mqtt_client.connect()
    except Exception as e:
        logger.log_debug(f"Failed to start mqtt client {e}")
        setup_fail(f"Failed to connect with mqtt broker: {config.connection.mqtt.server}.", 3)

    try:
        logger.log_debug(f"Configuring temperature device: {config.devices.temperature_sensor.id}")
        temperature_sensor = TemperatureSensorFactory(config, mqtt_client, logger).create()
        devices.append(temperature_sensor)

        for device_config in config.devices.soil_moisture_sensors:
            logger.log_debug(f"Configuring soil moisture device: {device_config.id}")
            soil_moisture_sensor = SoilMoistureSensorFactory(config, device_config, mqtt_client, logger).create()
            devices.append(soil_moisture_sensor)

    except Exception as e:
        logger.log_debug(f"Failed to configure devices {e}")
        setup_fail(f"Failed to configure devices: {config.devices}.", 3)

    try:
        application = App(devices, config, connection, mqtt_client, logger)
        application.start()
    except OSError as e:
        logger.log_error(str(e))
    except BaseException as e:
        logger.log_error(str(e))
    finally:
        setup_fail("Device unexpectedly leaved main loop.", 4)
