import numpy
from scipy import stats
import matplotlib.pyplot as plt

speed = [120,112,111,123,80,68,91,111,43,55,111,54,87,100,101,102,86,98]
speed_sorted = sorted(speed)

x_mean = numpy.mean(speed)
x_median = numpy.median(speed_sorted)
x_mode = stats.mode(speed)
x_std = numpy.std(speed)
x_vaiance = numpy.var(speed)

print("Avarage: " + str(x_mean))
print("Median: " + str(x_median))
print("Middle pice: " + str(x_mode))
print("Standard deviation: " + str(x_std))
print("variance: " + str(x_vaiance))

print("\nAGE DATASET")
ages = [5,31,43,48,50,41,7,11,15,39,80,82,32,2,8,6,25,36,27,61,31]

x_percentile_75 = numpy.percentile(ages,75)
x_percentile_90 = numpy.percentile(ages,90)

print("percentile 75: " + str(x_percentile_75))
print("percentile 90: " + str(x_percentile_90))

print("\n Generate random datasets")

# rand_dataset = numpy.random.uniform(0.0, 8.0, 100000)
# rand_normal = numpy.random.normal(5.0, 1.0, 100000)

# x_rand = rand_normal

# print(x_rand)
# plt.hist(x_rand, 100)
# plt.show()

scatter_x = [5,7,8,7,2,17,2,9,4,11,12,9,6]
scatter_y = [99,86,87,88,111,86,103,87,94,78,77,85,86]

slope, intercept, r, p, std_err = stats.linregress(scatter_x, scatter_y)

def myfunc(x):
    return slope * x + intercept

mymodel = list(map(myfunc, scatter_x))
print("relations: " + str(r))

speed_predict = myfunc(10)
print(speed_predict)
# rand_normal_x = numpy.random.normal(5.0, 1.0, 1000)
# rand_normal_y = numpy.random.normal(10.0, 2.0, 1000)

# plt.scatter(scatter_x, scatter_y)
# plt.plot(scatter_x, mymodel)
# plt.show()


# for s in speed_sorted:
#     print(s)