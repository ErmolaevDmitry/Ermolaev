import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

settings = np.loadtxt('settings.txt')
dt = 1 / settings[0]
step = settings[1]

data = np.loadtxt('data.txt')

data *= step
t = np.arange(0.0, (data.size) * dt, dt)

fig, ax = plt.subplots()
ax.set_xlabel("Время, с")
ax.set_ylabel("Напряжение, В")
ax.set_title("Процесс зарядки и разрядки конденсатора в RC-цепи", loc="center")
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
ax.minorticks_on()
ax.grid(which='major', color='gray')
ax.grid(which='minor', color='gray', alpha=0.5, linestyle='--') 

m = data.argmax()
ax.text(67, 2.5, "Время зарядки {:.2f} с".format(m*dt))
ax.text(67, 2.3, "Время разрядки {:.2f} с".format(data.size*dt - m*dt))

ax.plot(t, data, c='b', linewidth = 1.0, marker='o', markevery=200, mfc='b', ms=5, label='U(t)')
#ax.scatter(t[::200], data[::200], marker='o', c='b', s = 15)
ax.legend()

fig.savefig("test.svg")
plt.show()
