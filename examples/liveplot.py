import matplotlib.pyplot as plt
import random
from collections import deque
import time

class LivePlot:
    def __init__(self,miny=0,maxy=100,max_len=100):
        self.max_len = max_len
        
        self.data  = deque(maxlen=max_len)
        self.itnum = deque(maxlen=max_len)
        self.n = 0

        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [])
        
        self.ax.set_xlim(0, max_len)
        self.ax.set_ylim(miny, maxy)

        self.ax.grid(True)

    def set_lims(self, miny, maxy): 
        self.ax.set_ylim(miny, maxy)

    def add_data(self, newdata):
        self.itnum.append(self.n)
        self.data.append(newdata)
        
        self.line.set_xdata(self.itnum)
        self.line.set_ydata(self.data)

        if self.n > self.max_len:
            self.ax.set_xlim(self.n - self.max_len, self.n)        
        
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        self.n += 1

