import numpy
import pandas
import seaborn
from matplotlib import pyplot
from datetime import datetime

def semilog(series, title):
    time = [datetime.utcfromtimestamp(timestamp) for timestamp in series.index]
    pyplot.figure(figsize=(8, 5), dpi=80)
    pyplot.plot(time, series.values)
    pyplot.ylabel(series.name)
    pyplot.xlabel('Time')
    pyplot.title(title)
    pyplot.yscale('log')

def linear(series, title):
    time = [datetime.utcfromtimestamp(timestamp) for timestamp in series.index]
    pyplot.figure(figsize=(8, 5), dpi=80)
    pyplot.plot(time, series.values)
    pyplot.ylabel(series.name)
    pyplot.xlabel('Time')
    pyplot.title(title)
