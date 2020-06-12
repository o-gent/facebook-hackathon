import logging

def setup_logger(name, log_file, level=logging.INFO):
    """
    Creates a logger context
    """
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    stream = logging.StreamHandler()
    
    handler.setFormatter(formatter)
    stream.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    logger.addHandler(handler)
    logger.addHandler(stream)

    return logger
