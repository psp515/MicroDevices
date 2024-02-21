from abstractions.device import Device
from features.configuration.configuration import Configuration, DeviceConfiguration
from features.mqtt_clients.base_client import MqttClient
from loggers.logger import Logger
import machine
import ujson


class AnalogSoilMoistureSensor(Device):
    def __init__(self, config: Configuration,
                 device_config: DeviceConfiguration,
                 mqtt_client: MqttClient,
                 logger: Logger):
        super().__init__(config, device_config, mqtt_client, logger)
        self._adc = machine.ADC(device_config.data_pin)
        self._last_moisture = None

    def loop(self):
        try:
            moisture = self._calculate_moisture()

            if self.push_next or self._should_update_moisture(moisture):
                payload = self._create_payload(moisture)
                self.client.publish(self.update_config_topic, payload)
                self.push_next = False

        except BaseException as e:
            self.logger.log_debug(f"Exception in dht11 temperature sensor loop: {e}")
            self.logger.log_error(f"Dht11 sensor with id {self.id} unexpectedly failed.")

    def _create_payload(self, moisture):
        data = {
            "device": self.device_config.id,
            "moisture": {
                "value": moisture,
                "unit": self.device_config.threshold.unit
            },
        }

        return ujson.dumps(data)

    def _should_update_moisture(self, moisture):
        if self.device_config.threshold.type == "percent":
            if abs(self._last_moisture - moisture) > self.device_config.temp_threshold.value:
                self._last_moisture = moisture
                return True

        return False

    def _calculate_moisture(self):
        value = self._adc.read_u16()
        factor = 100 / 655535
        return int(value * factor)
