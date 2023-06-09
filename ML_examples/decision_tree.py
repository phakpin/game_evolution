import pandas
from sklearn import tree
import pydotplus
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import matplotlib.image as pltimmg

df = pandas.read_csv("film.csv")

d = {'UK': 0, 'USA': 1, 'N': 2}
df['Nationality'] = df['Nationality'].map(d)
d = {'YES': 1, 'NO': 0}
df['Go'] = df['Go'].map(d)

features = ['Age', 'Experience', 'Rank', 'Nationality']

X = df[features]
y = df['Go']

dtree = DecisionTreeClassifier()
dtree = dtree.fit(X, y)

print(dtree.predict([[40, 10, 6, 1]]))
# data = tree.export_graphviz(dtree, out_file=None, feature_names=features)

# graph = pydotplus.graph_from_dot_data(data)
# graph.write_png('mydecisions.png')

# img=pltimmg.imread('mydecisions.png')
# imgplot = plt.imshow(img)
# plt.show()

# print(X)
# print(y)

# print(df)