import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
import sys

plt.style.use('seaborn')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ax2 = ax1.twinx()

def deltas(xs):
    dx = []
    last = 0
    for x in xs:
        dx.append(x - last)
        last = x
    return dx


day = sys.argv[1]

def animation(i):
    filename = "file:///C:/Users/awarm/Documents/GitHub/aoc/curves/data/2022/day{}.csv".format(day)
    data = pd.read_csv(filename)  #, skiprows=lambda x: x%6!=0)
    if i == 0:
        return

    x = []
    y = []
    x = data[0:i]["minutes"]
    y1 = data[0:i]["both"]
    y2 = data[0:i]["half"]
    y3 = deltas(y1)

    ax1.clear()
    ax2.clear()

    color='tab:red'
    ax1.set_xlabel('time (min)')
    ax1.set_ylabel('Full completed', color=color)
    line1 = ax1.plot(x, y1, label='Full completed', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    yMax = int(max([max(data[0:i]["both"]), max(data[0:i]["half"])]) * 1.1)
    ax1.set_ylim([0, yMax])
    ax1.set_xlim([0, data["minutes"].iloc[-1]])

    color='tab:green'
    line2 = ax1.plot(x, y2, label='First part only', color=color)

    color='tab:blue'
    ax2.set_ylabel('Deltas', color=color)
    bars1 = ax2.bar(x, y3, label="deltas", color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim([0, 1000])

    fig.tight_layout()
    # ax1.legend([line1, line2, bars1], ['Full', 'First only', 'Deltas'], loc='upper left')
    # ax.set_xlim([data["seconds"].iloc[0], data["seconds"].iloc[-1]])

animation = FuncAnimation(fig, func=animation, interval=16)
plt.show()
