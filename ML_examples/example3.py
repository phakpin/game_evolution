import numpy
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler
import pandas
scale = StandardScaler()

df = pandas.read_csv("cars2.csv")

X = df[['Weight', 'Volume']]
y = df['CO2']

scaledX = scale.fit_transform(X)

# print(scaledX)

regr = linear_model.LinearRegression()
regr.fit(scaledX, y)

scaled = scale.transform([[2300, 1.3]])

# print(regr.coef_)

predictedCO2 = regr.predict([scaled[0]])
print(predictedCO2)

# x = [89,43,36,36,95,10,66,34,38,20,26,29,48,64,6,5,36,66,72,40]
# y = [21,46,3,35,67,95,53,72,58,10,26,34,90,33,38,20,56,2,47,15]

# mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))

# print(r2_score(y, mymodel(x)))

# myline = numpy.linspace(2, 95, 100)

# plt.scatter(x, y)
# plt.plot(myline, mymodel(myline))
# plt.show()