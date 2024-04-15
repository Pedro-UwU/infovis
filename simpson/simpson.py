import matplotlib.pyplot as plt
import numpy as np
import csv

with open("./simpson.csv") as f:
    csv_reader = csv.reader(f)
    data = list(csv_reader)
    data = data[1:]

c = [row[2] for row in data]
separated_data = dict()
classes = list(set(c))

for clazz in classes:
    x = [float(row[0]) for row in data if row[2] == clazz]
    y = [float(row[1]) for row in data if row[2] == clazz]

    # Calculate tendency line
    x = np.array(x)
    y = np.array(y)
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    separated_data[clazz] = (x, y, m, c)

for clazz, (x, y, m, c) in separated_data.items():
    plt.scatter(x, y, label=clazz, s=30, alpha=0.5, edgecolors='none')
    plt.plot(x, m*x + c, label=f"{clazz} tendency line")

plt.grid()
plt.show()
