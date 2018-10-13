from pandas import unique
from pandas import read_csv
from sklearn.preprocessing import normalize
from matplotlib import pyplot
import sys

# load dataset
df = read_csv(sys.argv[1], header=0, index_col=None)

## plot data per person
window = range(0, df.shape[0])

g_x = df.values[window, 0]
pyplot.plot(window, g_x)

g_y = df.values[window, 1]
pyplot.plot(window, g_y)

g_z = df.values[window, 2]
pyplot.plot(window, g_z)

acc_x = df.values[window, 3]
pyplot.plot(window, acc_x)

acc_y = df.values[window, 4]
pyplot.plot(window, acc_y)

acc_z = df.values[window, 5]
pyplot.plot(window, acc_z)



pyplot.show()