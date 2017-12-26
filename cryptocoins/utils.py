from datetime import timedelta, datetime
import logging


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

def setup_logging(file_name=None, max_bytes = 200000000, backup_count = 5):
    logger = logging.getLogger("cryptocoins")
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('(%(levelname)s|%(asctime)s|%(module)s|%(filename)s) %(message)s')
    if file_name is None:
        handler = RotatingFileHandler(file_name, "a", max_bytes, backup_count)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info("LOGGING to {file_name}")
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info("LOGGING to stdout")
    return logger
