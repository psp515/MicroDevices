from loggers.logger import Logger
from loggers.logger import LoggerLevels
from features.configuration.configuration import Configuration

import gc
import ujson
import sys

if __name__ == '__main__':
    gc.collect()

    logger = Logger(LoggerLevels.DEBUG)
    config = None
    connection = None
    connectionMqtt = None
    app = None

    logger.log_info("Starting parsing configuration.")

    try:
        with open('device_settings.json', 'r') as file:
            json_file = file.read()

        config_data = ujson.loads(json_file)
        config = Configuration(config_data)
    except Exception as e:
        logger.log_error(str(e))
        sys.exit(1)

    logger.log_info("Finished parsing configuration. Updating logger")

"""
    try:
        # TODO when starting try to establish blt connection to update configuration
        pass
    except:
        pass

    try:
        # Configure Devices
        pass
    except:
        pass

    try:
        #wlan_config = read_json("config/secrets.json")
        #validate_wlan_config(wlan_config)
        #wlan = network.WLAN(network.STA_IF)
        #wlan.active(True)
        #wlan.connect(wlan_config["ssid"], wlan_config["password"])
        #wait_for_connection(wlan, logger)
        pass
    except:
        pass

    try:
        #hivemq_config = read_json("config/hivemq.json")
        #validate_hivemq_config(hivemq_config)
        #mqtt_client = HivemqMQTTClient(hivemq_config, logger, device_state)
        #mqtt_client.connect()
        #mqtt_topics = configure_mqtt(mqtt_client)
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
