import logging
import logging.handlers

# logger instance
logger = logging.getLogger(__name__)

# formatter
formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)s] - == %(message)s')

# Hander
streamHandler = logging.StreamHandler()
fileHandler = logging.handlers.TimedRotatingFileHandler('./crawling-logfile.log', when='midnight', interval=1, encoding='utf-8')
fileHandler.suffix = '%Y%m%d'

streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

logger.setLevel(level=logging.DEBUG)