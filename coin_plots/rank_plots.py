import numpy
import pandas
import seaborn
from matplotlib import pyplot


def count_and_rank(data_frame, aggregated_column, count_column):
    count_series = data_frame[count_column].groupby(data_frame[aggregated_column]).count().sort_values(ascending=False)
    count_data_frame = count_series.to_frame()
    count_data_frame['rank'] = count_data_frame[count_column].rank(ascending=False, method="dense")
    return count_data_frame


def count_and_rank_plot(data_frame):
    index_name = data_frame.index.name
    nbins = numpy.max(data_frame['rank'].values) + 1.0
    ncoins = numpy.min([len(data_frame), 10])
    bins = [0.5 + i for i in numpy.arange(0.0, nbins)]
    pyplot.hist(data_frame['rank'].values, bins=bins)
    pyplot.ylabel('Count')
    pyplot.xlabel('Rank')
    pyplot.yscale('log')
    pyplot.title(index_name + " Rank Distribution")
    xoffset = 0.05
    yoffset = 0.9
    dyoffset = 0.05
    for i in range(0, ncoins):
        y = yoffset - dyoffset * i
        coin_symbol = data_frame.index[i]
        count = data_frame.iloc[i, 0]
        pyplot.annotate(f"{coin_symbol}: {count}", (xoffset, y), xycoords='axes fraction')
