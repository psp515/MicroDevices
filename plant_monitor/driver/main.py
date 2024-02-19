from machine import reset
from loggers.logger_factory import LoggerFactory
from features.configuration.configuration import Configuration
from features.network_connection.wifi_connector import WiFiConnection
from features.clients.client_factory import MqttFactory

import gc
import ujson
import sys
import globals


def setup_fail(message: str, debug_message: str):
    logger.log_error(message)
    if config.mode == globals.DEBUG:
        logger.log_debug("")
        sys.exit(2)
    reset()


if __name__ == '__main__':
    gc.collect()

    logger = LoggerFactory.default_logger()
    config = None
    mqtt_client = None
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
        logger.log_debug(config_data)
        sys.exit(1)

    connection = WiFiConnection(config.connection.wifi, logger)
    result = connection.connect()

    if not result:
        setup_fail(f"Failed to connect with ssid: {config.connection.wifi.ssid}.")

    try:
        mqtt_config = config.connection.mqtt
        mqtt_client = MqttFactory(mqtt_config).create()
        

    except:
        pass

"""
        
    try:
        # Configure Devices
        pass
    except:
        pass

    try:
        # Run Application
        pass
    except OSError as e:
        logger.log_error(str(e))
    except BaseException as e:
        logger.log_error(str(e))
    finally:
        pass
        #if not DEBUG:
        #    sleep(3)
        #    reset()
"""