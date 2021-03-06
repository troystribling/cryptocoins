from datetime import timedelta, datetime
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)


def day_dir(file_date):
    return file_date.strftime('%Y%m%d')


def date_prefix(file_date):
    return file_date.strftime('%Y%m%d-%H%M%S-')


def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + timedelta(n)


def valid_params(expected_params, params):
    for expected_param in expected_params:
        if expected_param not in params:
            logger.error(f"'{expected_param}' KEY IS MISSING FROM {params}")
            return False
    return True

def null_param_if_missing(expected_params, params):
    for expected_param in expected_params:
        if expected_param not in params:
            logger.warn(f"'{expected_param}' KEY IS MISSING FROM {params}")
            params[expected_param] = None

def setup_logging(file_name=None, max_bytes=200000000, backup_count=5):
    logger = logging.getLogger("cryptocoins")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('(%(levelname)s|%(asctime)s|%(module)s|%(filename)s, %(lineno)s) %(message)s')
    if file_name is not None:
        handler = RotatingFileHandler(file_name, "a", max_bytes, backup_count)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info(f"LOGGING to {file_name}")
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info("LOGGING to stdout")
    return logger
