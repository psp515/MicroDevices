from features.configuration.configuration import Configuration, DeviceConfiguration


class Device:
    def __init__(self, config: Configuration, device_config: DeviceConfiguration):
        self.config = config
        self.device_config = device_config

    @property
    def id(self):
        return self.device_config.id

    def loop(self):
        pass
