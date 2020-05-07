import numpy as np
import matplotlib
import matplotlib.pyplot as plt

infected = ["porto","lisboa", "braga", "aveiro", "faro", "guarda", "leiria"]
safe = ["taxi1","taxi2", "taxi3", "taxi4", "taxi5", "taxi6", "taxi7"]

probability = np.array([[0.8, 0.4, 0.5, 0.9, 0.0, 0.0, 0.0],
                [0.4, 0.0, 0.0, 1.0, 0.7, 0.0, 0.0],
                [1.0, 0.4, 0.8, 0.3, 1.0, 0.4, 0.0],
                [0.6, 0.0, 0.3, 0.0, 0.1, 0.0, 0.0],
                [0.7, 1.0, 0.6, 0.6, 0.2, 0.2, 0.0],
                [1.0, 1.0, 0.0, 0.0, 0.0, 0.2, 0.1],
                [0.1, 0.0, 0.0, 1.0, 0.0, 1.0, 0.3]])

fig, ax = plt.subplots()
img = ax.imshow(probability)

ax.set_xticks(np.arange(len(infected)))
ax.set_xticklabels(infected)

plt.setp(ax.get_xticklabels(),rotation=45, ha="right", rotation_mode="anchor")

for i in range(len(infected)):
    for j in range(len(safe)):
        text = ax.text(j, i, probability[i, j],
                       ha="center", va="center", color="w")

ax.set_title("Infected evolution")
fig.tight_layout()
plt.show()

