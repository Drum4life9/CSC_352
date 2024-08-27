import graphviz
from sklearn.tree import DecisionTreeClassifier as dtc, plot_tree, export_graphviz
import numpy as np
import csv
import matplotlib.pyplot as plt

first = True
headers = []
rows = []

with open('web-page-phishing.csv', newline='') as file:
    reader = csv.reader(file, delimiter=',', quotechar='"')
    for row in reader:
        if first:
            first = False
            headers = row
        else:
            rows.append(list(map(int, row)))

last = lambda r: rows[r][-1]

results = []

for i in range(len(rows)):
    results.append(last(i))
    rows[i] = rows[i][0:len(rows[i]) - 1]

print(rows[0])

clf = dtc(max_depth=4)
clf = clf.fit(rows, results)


dot_data = export_graphviz(clf, out_file=None,
                           feature_names=headers[0:19],
                           filled=True, rounded=True,
                           special_characters=True, impurity=False,
                           leaves_parallel=False,
                           proportion=True)
graph = graphviz.Source(dot_data)
graph.render("classification")
