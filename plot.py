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





def plot_alphas(x, y):

    fig = plt.figure()
    plt.xlabel('alpha', fontsize=15)
    plt.ylabel('# of trades', fontsize=15)
    ax1 = fig.gca()

    ax1.plot(x, y, label='num_trades')

    # plt.legend()
    ax1.set_title('trades completed vs. learning rate alpha')

    fig.savefig('./plots/alpha_trades.png')

    # fig = plt.figure()
    # plt.xlabel('alpha', fontsize=15)
    # plt.ylabel('final utility', fontsize=15)
    # ax1 = fig.gca()
    #
    # ax1.plot(x, y, label='utility')
    #
    # # plt.legend()
    # ax1.set_title('utility vs. learning rate alpha')
    #
    # fig.savefig('./plots/alpha_utility.png')







x = [0, 0.05, 0.15, 0.25, 0.4, 0.5, 0.6, 0.75, 0.9, 1]
y = [-74.24893612595159, 33.374945653985485, 32.60163478460832, 17.82062394953362, 18.309472760479547, 29.26954222141532, 22.734062903010926, 43.99451072600699, 47.59751547267195, 12.31049699064315]
y_2 = [637.7, 503.26, 360.56, 422.56, 366.9, 369.96, 443.36, 477.14, 432.02, 344.68]


# plot_alphas(x, y_2)



def plot_budgets(x, a, b, c, d, e):

    fig = plt.figure()
    plt.xlabel('budget ($)', fontsize=15)
    plt.ylabel('# of trades', fontsize=15)
    ax1 = fig.gca()

    ax1.plot(x, [i / 2 for i in a], 'p--', label='AMM b=10e2')
    ax1.plot(x, [i / 2 for i in d], 'r--', label='AMM b=10e6')
    ax1.plot(x, [i / 2 for i in e], 'm--', label='AMM b=10e9')
    ax1.plot(x, [i / 2 for i in b], label='CDA')
    ax1.plot(x, [i / 2 for i in c], label='CDA+MM')



    plt.legend()
    ax1.set_title('budget vs. number of trades')

    fig.savefig('./plots/budget_trades.png')

    # fig = plt.figure()
    # plt.xlabel('alpha', fontsize=15)
    # plt.ylabel('final utility', fontsize=15)
    # ax1 = fig.gca()
    #
    # ax1.plot(x, y, label='utility')
    #
    # # plt.legend()
    # ax1.set_title('utility vs. learning rate alpha')
    #
    # fig.savefig('./plots/alpha_utility.png')



x = [1, 20, 40, 60, 80, 100]
a = [280, 2901, 4971, 4657, 4502, 4962]
b = [152,3848, 7210, 8980, 8858, 8416]
c = [1316, 4584, 6970, 7656, 9164, 9326]
d = [1077, 1790, 2327, 3100, 2400, 2600]
e = [1115, 1690, 2227, 2400, 2900, 2300]


plot_budgets(x, a, b, c, d, e)
