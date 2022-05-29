import numpy as np
import math
import matplotlib.pyplot as plt

def temperature(year) -> float:
    return math.atan(-0.0012*(year**3) + 0.4*(year**2) + 0.616*year + 6120) + 0.65*math.sin(0.24*year + 1.23) - 0.27*math.cos(0.21*year - 0.17) - math.sin(0.34*year + 0.16)/(1 + 0.03*(year - 370.5)**2)

# x = np.linspace(0, 4*np.pi, 1000)
# y = np.sin(x)
#
# fig, ax = plt.subplots() # or you can go like that
# ax.plot(x, y)
#
# plt.show()

# x = [-7.0, -5.0, -3.0, -1.0, 0, 1, 3, 5, 7]
# sin_y = [math.sin(t) for t in x]
# cos_y = [math.cos(t) for t in x]
# plt.title("harmonic funs: sine and cosine")
# plt.plot(x, x, '--', x, [1]*len(x), '--', x, [-1]*len(x), '--', x, sin_y, x, cos_y)
# plt.show()

t = [i for i in range(0, 1001)]
temperature_fig = [temperature(x) for x in t]

a = 0.0
b = 1000.0
eps = 0.0001

while ((b-a) >= eps):
    mid = (a + b) / 2

    if (temperature(mid) == 0.0):
        break
    else:
        if temperature(a)*temperature(mid) < 0.0:
            b = mid
        elif temperature(b)*temperature(mid) < 0.0:
            a = mid

plt.title("Average Earth Temperature")
plt.xlabel("Year")
plt.ylabel("Temperature")
plt.plot(t, temperature_fig, t, [0]*len(t), '--')
plt.plot(mid, temperature(mid), 'ro')
print(mid)

plt.show()

