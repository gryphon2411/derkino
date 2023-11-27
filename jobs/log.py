import logging
import ecs_logging


def get_logger(name):
    # Get the Logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Add an ECS formatter to the Handler
    handler = logging.StreamHandler()
    handler.setFormatter(ecs_logging.StdlibFormatter())
    logger.addHandler(handler)

    return logger
