# %%
import numpy
from matplotlib import pyplot
from scipy import stats

%matplotlib inline

# %%


def parabola(x):
    return 2.0 * numpy.power(x, 2) + 4


def linear(x):
    return 2.0 * x + 4


def gauss(x):
    return stats.norm.pdf(x, 2.0, 2.0)


def metropolis(p, nsample=10000):
    x = 0.0
    samples = numpy.zeros(nsample)

    for i in numpy.arange(nsample):
        x_star = x + numpy.random.normal()
        reject = numpy.random.rand()
        if reject < p(x_star) / p(x):
            x = x_star
        samples[i] = x

    return samples


def sample_plot(samples):
    figure, axis = pyplot.subplots(figsize=(12, 5))
    axis.set_xlabel("Sample")
    axis.set_ylabel("Value")
    axis.set_title("Metropolis Sampling")
    axis.grid(True, zorder=5)
    axis.hist(samples, 30, density=True, color="#348ABD", alpha=0.6, edgecolor="#348ABD", lw="3", zorder=10)

# %%

samples = metropolis(linear, nsample=100000)
sample_plot(samples)

# %%

samples = metropolis(parabola, nsample=100000)
sample_plot(samples)


# %%

samples = metropolis(gauss, nsample=10000)
sample_plot(samples)
