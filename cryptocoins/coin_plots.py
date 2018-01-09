import numpy
import matplotlib.pyplot as pyplot
import seaborn

def to_symbol_count(data):
    seaborn.set(style="ticks")
    seaborn.lmplot(x="x", y="y", col="dataset", hue="dataset", data=data, col_wrap=2, ci=None, palette="muted", size=4, scatter_kws={"s": 50, "alpha": 1})
