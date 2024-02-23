from abstractions.device import Device
from features.configuration.configuration import Configuration, DeviceConfiguration
from features.mqtt_clients.base_client import MqttClient
from loggers.logger import Logger
import machine
import ujson
from utime import ticks_ms, ticks_diff


class AnalogSoilMoistureSensor(Device):
    def __init__(self, config: Configuration,
                 device_config: DeviceConfiguration,
                 mqtt_client: MqttClient,
                 logger: Logger):
        super().__init__(config, device_config, mqtt_client, logger)
        self._adc = machine.ADC(device_config.data_pin)
        self._last_moisture = None
        self._last_read = ticks_ms()

    def loop(self):
        try:
            self.logger.log_info("Starting loop of sms analog sensor.")
            moisture = self._calculate_moisture()

            if self.push_next or self._should_update_moisture(moisture):
                self.logger.log_debug("Sending update message in sms analog sensor.")
                payload = self._create_payload(moisture)
                topic = self.device_config.topic
                self.mqtt_client.publish(self.device_config.topic, payload)
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
        if self._last_moisture is None:
            self._last_moisture = moisture
            return True

        if self.device_config.threshold.type == "time":
            # TODO
            read = ticks_ms()
            if abs(ticks_diff(read, self._last_read)) > self.device_config.threshold.value:
                self._last_read = read
                return True

        if self.device_config.threshold.type == "percent":
            if abs(self._last_moisture - moisture) > self.device_config.threshold.value:
                self._last_moisture = moisture
                return True

        return False

    def _calculate_moisture(self):
        moistures = [self._measure_moisture() for _ in range(10)]
        return sum(moistures) / len(moistures)

    def _measure_moisture(self):
        value = self._adc.read_u16()
        value = value // 256
        m = -0.5
        b = 127

        scaled_value = m * value + b
        scaled_value = max(0, min(100, scaled_value))

        return scaled_value
