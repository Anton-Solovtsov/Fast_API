import logging

def conf_logging():
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s",
            datefmt='%d-%m-%Y %H:%M:%S'
        )
    logging.getLogger('app').setLevel(logging.INFO)

