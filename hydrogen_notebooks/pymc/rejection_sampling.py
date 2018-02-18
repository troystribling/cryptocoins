# %%
%load_ext autoreload
%autoreload 2

%aimport numpy
%aimport sympy

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

def samples_plot(cdf, x):
    figure, axis = pyplot

# %%
# Inverse CDF Descrete random variables


x = sympy.symbols('x')
sympy.Heaviside(0, 1)
steps = [sympy.Heaviside(x - i + 1, 1) for i in range(1, 7)]

steps[0]
steps[0].subs(x, 2)

cdf = sum(steps) / 6
cdf.subs(x, 3)

sympy.plot(cdf, (x, 0, 6), ylabel="CDF(x)", xlabel='x', ylim=(0, 1))

# %%
# The inverse of the heavyside distribution is given by
x = sympy.symbols('x')
intervals = [(0, x < 0), (1, sympy.Interval(0, 1 / 6).contains(x)), (2, sympy.Interval(1 / 6, 2 / 6).contains(x)), (3, sympy.Interval(2 / 6, 3 / 6).contains(x)), (4, sympy.Interval(3 / 6, 4 / 6).contains(x)), (4, sympy.Interval(4 / 6, 5 / 6).contains(x)), (6, x > 5 / 6)]
inv_cdf = sympy.Piecewise(*intervals)
samples = [inv_cdf.subs(x, i) for i in rand(10)]
