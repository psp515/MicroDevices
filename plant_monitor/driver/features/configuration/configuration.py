import json


class Configuration:
    def __init__(self, config_data):
        self.mode = config_data.get("mode")
        self.baseDeviceTopic = config_data.get("baseDeviceTopic")
        self.connection = Connection(config_data.get("Connection", {}))
        self.logs = Logs(config_data.get("Logs", {}))
        self.devices = Devices(config_data.get("Devices", {}))


class Connection:
    def __init__(self, connection_data):
        self.wifi = Wifi(connection_data.get("Wifi", {}))
        self.mqtt = Mqtt(connection_data.get("MQTT", {}))


class Wifi:
    def __init__(self, wifi_data):
        self.ssid = wifi_data.get("ssid")
        self.password = wifi_data.get("password")


class Mqtt:
    def __init__(self, mqtt_data):
        self.type = mqtt_data.get("type")
        self.server = mqtt_data.get("server")
        self.port = mqtt_data.get("port")
        self.user = mqtt_data.get("user")
        self.password = mqtt_data.get("password")
        self.clientId = mqtt_data.get("clientId")
        self.ssl = mqtt_data.get("ssl")


class Logs:
    def __init__(self, logs_data):
        self.local = LogType(logs_data.get("Local", {}))
        self.remote = LogType(logs_data.get("Remote", {}))


class LogType:
    def __init__(self, log_data):
        self.localFile = log_data.get("localFile")
        self.level = log_data.get("level")
        self.enabled = log_data.get("enabled")


class Devices:
    def __init__(self, devices_data):
        self.temperatureSensor = Device(devices_data.get("temperatureSensor", {}))
        self.soilMoistureSensors = [Device(sensor_data) for sensor_data in devices_data.get("SoilMoistureSensors", [])]


class Device:
    def __init__(self, device_data):
        self.type = device_data.get("type")
        self.dataPin = device_data.get("dataPin")
        self.groundPin = device_data.get("groundPin")
        self.vccPin = device_data.get("vccPin")
        self.threshold = Threshold(device_data.get("treshold", {}))
        self.temperatureUnit = device_data.get("temperatureUnit")


class Threshold:
    def __init__(self, threshold_data):
        self.type = threshold_data.get("type")
        self.value = threshold_data.get("value")
        self.unit = threshold_data.get("unit")