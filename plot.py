import matplotlib.pyplot as plt
import numpy as np


def line_chart(x, y, title):
    fig = plt.figure()
    ax1 = fig.gca()

    ax1.plot(x, y)
    ax1.set_title(title)
    fig.savefig('./line_chart.png')



def histogram(x, title):
    fig = plt.figure()
    ax1 = fig.gca()

    ax1.hist(x)
    ax1.set_title(title)
    fig.savefig('./histogram.png')
