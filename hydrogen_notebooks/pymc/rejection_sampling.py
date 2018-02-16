# %%
import numpy
from matplotlib import pyplot
from scipy import stats

%matplotlib inline

# %%


def parabola(x):
    if x < 0.0 or x > 1.0:
        return None
    return 3.0 * numpy.power(x, 2)


def linear(x):
    if x < 0.0 or x > 1.0:
        return None
    return 2.0 * x


# %%
