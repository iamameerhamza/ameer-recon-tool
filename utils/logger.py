import logging

def setup_logger(level=logging.INFO):
    logger = logging.getLogger("ReconTool")
    logger.setLevel(level)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)

        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
