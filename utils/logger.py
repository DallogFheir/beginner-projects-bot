import logging

stream_handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s : %(message)s")
stream_handler.setFormatter(formatter)
logger = logging.getLogger("logger")
logger.addHandler(stream_handler)
