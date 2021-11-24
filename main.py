import matplotlib.pyplot as plt
import numpy as np

x = np.array(np.linspace(0, 2*3.14, num=1000))
y = np.sin(x)

plt.scatter(x, y)
plt.show()
