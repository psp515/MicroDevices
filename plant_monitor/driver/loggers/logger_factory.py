from logger import Logger
from enums.logger_levels import LoggerLevels
from features.configuration.configuration import Logs


class LoggerFactory:

    @staticmethod
    def default_logger():
        return Logger(LoggerLevels.DEBUG)

    @staticmethod
    def create_logger(self, logs_config: Logs):
        pass # TODO if logs.local.enabled

