import numpy as np; np.random.seed(32)
from matplotlib.path import Path
from matplotlib.textpath import TextToPath
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt

fp = FontProperties(fname=r"./Font Awesome 5 Free-Solid-900.otf")

symbols = dict(taxi = "\uf1ba",car_side= "\uf5e4")

fig, ax = plt.subplots()

def get_marker(symbol):
    v, codes = TextToPath().get_text_path(fp, symbol)
    v = np.array(v)
    mean = np.mean([np.max(v,axis=0), np.min(v, axis=0)], axis=0)
    return Path(v-mean, codes, closed=False)

x = np.random.randn(4,10)
c = np.random.rand(10)
s = np.random.randint(120,500, size=10)

plt.scatter(*x[:2], s=s, c=c, marker=get_marker(symbols["car_side"]), 
            edgecolors="none", linewidth=2)

plt.show()