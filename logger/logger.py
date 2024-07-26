import os
import logging
from logger import settings


class Logger:

    def __init__(self, logger_name, level=logging.DEBUG):
        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(settings.FORMAT)
        current_dir = os.path.dirname(__file__)
        repo_dir = os.path.abspath(os.path.join(current_dir, '..'))
        log_directory = os.path.abspath(os.path.join(repo_dir, "logs"))

        if not os.path.isdir(log_directory):
            os.mkdir(log_directory)
        log_file_path = os.path.join(log_directory, f"{logger_name}.log")

        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stdout_handler = logging.StreamHandler()
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)

    def error(self, msg):
        self.logger.error(msg, extra={'unit': self.logger_name})

    def info(self, msg):
        self.logger.info(msg, extra={'unit': self.logger_name})

    def debug(self, msg):
        self.logger.debug(msg, extra={'unit': self.logger_name})


if __name__ == '__main__':
    logger = Logger('test')
    logger.info('Test message.')
