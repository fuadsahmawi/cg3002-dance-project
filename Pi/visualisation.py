from pandas import unique
from pandas import read_csv
from sklearn.preprocessing import normalize
from matplotlib import pyplot
import sys

# load dataset
df = read_csv(sys.argv[1], header=0, index_col=None)

## plot data per person
window = range(0, df.shape[0])

pyplot.subplot(2,1,1)

g1_x = df.values[window, 0]
pyplot.plot(window, g1_x)

g1_y = df.values[window, 1]
pyplot.plot(window, g1_y)

g1_z = df.values[window, 2]
pyplot.plot(window, g1_z)

acc1_x = df.values[window, 3]
pyplot.plot(window, acc1_x)

acc1_y = df.values[window, 4]
pyplot.plot(window, acc1_y)

acc1_z = df.values[window, 5]
pyplot.plot(window, acc1_z)
pyplot.title('Sensor 2')


pyplot.subplot(2,1,2)

g2_x = df.values[window, 6]
pyplot.plot(window, g2_x)

g2_y = df.values[window, 7]
pyplot.plot(window, g2_y)

g2_z = df.values[window, 8]
pyplot.plot(window, g2_z)

acc2_x = df.values[window, 9]
pyplot.plot(window, acc2_x)

acc2_y = df.values[window, 10]
pyplot.plot(window, acc2_y)

acc2_z = df.values[window, 11]
pyplot.plot(window, acc2_z)
pyplot.title('Sensor 3')

pyplot.show()