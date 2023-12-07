import matplotlib.pyplot as plt
import numpy as np


def line_chart(x, y, title, x_label='average utility ($)', y_label='# of Agents', file_name=None):
    fig = plt.figure()
    plt.xlabel(x_label, fontsize=15)
    plt.ylabel(y_label, fontsize=15)
    ax1 = fig.gca()
    ax1.plot(x, y)
    ax1.set_title(title)

    if file_name is not None:
        fig.savefig('./plots/' + file_name + '.png')
    else:
        fig.savefig('./plots/linechart.png')




def histogram(x, title, x_label='average utility ($)', y_label='# of Agents', file_name=None):
    fig = plt.figure()
    plt.xlabel(x_label, fontsize=15)
    plt.ylabel(y_label, fontsize=15)
    ax1 = fig.gca()
    ax1.hist(x)
    ax1.set_title(title)

    if file_name is not None:
        fig.savefig('./plots/' + file_name + '.png')
    else:
        fig.savefig('./plots/histogram.png')




def mm_line_chart(x, y, y_labels, title, x_label='average utility ($)', y_label='# of Agents', file_name=None):
    fig = plt.figure()
    plt.xlabel(x_label, fontsize=15)
    plt.ylabel(y_label, fontsize=15)
    ax1 = fig.gca()
    # y is multidimensional, but all correspond to the same x
    for i, z in enumerate(y):
        ax1.plot(x, z, label=y_labels[i])

    plt.legend()
    ax1.set_title(title)

    if file_name is not None:
        fig.savefig('./plots/' + file_name + '.png')
    else:
        fig.savefig('./plots/mm_linechart.png')
