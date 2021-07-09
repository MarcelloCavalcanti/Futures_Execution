import logging
#from paths import CustomPaths


class Logger:

    @classmethod
    def get_logger(cls):
        """
        Initializes and configures a logger.
        :return: The python logger object.
        """
        logger = logging.getLogger('fflex_log')
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        #logger_path = CustomPaths.logger
        logger_path = 'C:/Users/MarcelloCavalcanti/Google Drive/Trading/Python/Models/Stochastic_Pair_Trading/Fasanara/Futures_Execution/Logs/fflex_log.log'
        handler = logging.FileHandler(logger_path, mode='a')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        return logger
