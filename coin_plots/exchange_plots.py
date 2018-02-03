import numpy
import pandas
import seaborn
from matplotlib import pyplot
from datetime import datetime

def exchanges(data_frame):
    time = datetime.utcfromtimestamp(data_frame.timestamp_epoc)
    exchange_rank = data_frame.index.values
    exchanges = data_frame['exchange'].values
    price = data_frame['close_price_24_hour'].values
    volume = data_frame['volume_from_24_hour'].values
    total_from_volume = sum(volume)
    volume_per_exchange = [exchange_volume / total_from_volume for exchange_volume in volume]
    title = f"{time.strftime('%Y/%m/%d')} {data_frame.from_symbol} to {data_frame.to_symbol}"
    figure, price_axis = pyplot.subplots(figsize=(12, 5), dpi=80)
    volume_axis = price_axis.twinx()
    price_axis.plot(exchange_rank, price, color='Blue')
    price_axis.set_ylabel('Price', color='Blue')
    price_axis.tick_params(axis='y', colors='Blue')
    price_axis.set_xlabel('Exchange')
    price_axis.set_xticks(exchange_rank)
    price_axis.set_xticklabels(exchanges, rotation='vertical')
    price_axis.set_title(title)
    volume_axis.set_ylabel("% Volume", color='Red')
    volume_axis.plot(exchange_rank, volume_per_exchange, color='Red')
    volume_axis.tick_params(axis='y', colors='Red')
