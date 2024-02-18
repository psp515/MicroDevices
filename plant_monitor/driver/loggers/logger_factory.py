from logger import Logger
from enums.logger_levels import LoggerLevels
from features.configuration.configuration import Logs
from features.configuration.configuration import LogType

class LoggerFactory:

    @staticmethod
    def default_logger():
        return Logger(LoggerLevels.DEBUG)

    @staticmethod
    def create_logger(self, logs_config: Logs):
        pass # if logs.local.enabled

