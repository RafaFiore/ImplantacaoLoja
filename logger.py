import logging


class Logger:
    def __init__(self):
        self.__filemode = 'a'
        self.__format = '%(asctime)s %(levelname)s %(message)s'

    def info(self, log_file, msg):
        level = logging.DEBUG
        logging.basicConfig(filename=log_file,
                            filemode=self.__filemode,
                            format=self.__format,
                            datefmt='%d-%m-%Y %H:%M:%S',
                            level=level)
        logging.info(msg)

    def error(self, log_file, msg):
        level = logging.ERROR
        logging.basicConfig(
            filename=log_file,
            filemode=self.__filemode,
            format=self.__format,
            level=level)
        logging.error(msg)
