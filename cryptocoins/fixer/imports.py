from cryptocoins.import_data import import_from_s3
import logging

from cryptocoins.models.forex_pairs_history import ForexPairsHistory

logger = logging.getLogger(__name__)

@import_from_s3(remote_dir='forex/fixer/usd_rates')
def import_from_usd_rates(data):
    if len(data) != 1:
        logger.error("DATA WRONG SIZE")
        return
    ForexPairsHistory.create_from_fixer_exchange_rate(data[0])
