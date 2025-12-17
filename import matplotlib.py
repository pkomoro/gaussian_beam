import matplotlib.pyplot as plt
import numpy as np

x, y = [1, 2], [1, 2]

# Default (looks big due to area & edge)
plt.figure(figsize=(6, 2))
plt.subplot(1, 3, 1)
plt.scatter(x, y)
plt.title('Default')

# Small Radius (s=4 is area for radius=2) with no edge
plt.subplot(1, 3, 2)
plt.scatter(x, y, s=4, linewidths=0)
plt.title('s=4, lw=0')

# Large Radius (s=100 is area for radius=10)
plt.subplot(1, 3, 3)
plt.scatter(x, y, s=100)
plt.title('s=100')

plt.tight_layout()
plt.show()