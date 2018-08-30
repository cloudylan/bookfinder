import matplotlib.pyplot as plot
from analysis import score
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from numpy import *


def histogram():
    allocations = score.score_allocation()

    count = [item.count for item in allocations]
    score_label = [item.label for item in allocations]

    plot.hist(score_label)
    plot.show()


def bar():
    allocations = score.score_allocation()
    count = [item.count for item in allocations]
    score_label = [item.label for item in allocations]
    colors = ['red', 'chartreuse', 'deepblue', 'plum', 'darkorange', 'c', 'lightskyblue', 'pink', 'lime', 'cyan']
    colors_2 = ['red', 'chartreuse', 'deepskyblue', 'plum', 'darkorange', 'c', 'lightskyblue', 'lime', 'm', 'yellow']

    # fig, ax = plot.subplots()

    xmajorLocator = MultipleLocator(1)
    xmajorFormatter = FormatStrFormatter('%1.1f')
    xminorLocator = MultipleLocator(0.5)

    ymajorLocator = MultipleLocator(100)
    ymajorFormatter = FormatStrFormatter('%1.1d')
    yminorLocator = MultipleLocator(50)

    # t = arange(0.0, 100.0, 1)
    # s = sin(0.1 * pi * t) * exp(-t * 0.01)

    ax = plot.subplot(111)  # 注意:一般都在ax中设置,不再plot中设置
    # plot(t, s, '--b*')

    # 设置主刻度标签的位置,标签文本的格式
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.xaxis.set_major_formatter(xmajorFormatter)

    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_major_formatter(ymajorFormatter)

    # 显示次刻度标签的位置,没有标签文本
    ax.xaxis.set_minor_locator(xminorLocator)
    ax.yaxis.set_minor_locator(yminorLocator)

    ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度

    ax.set_xlabel('Rating')
    ax.set_ylabel('Number')
    ax.set_title('Book Ratings Allocation')
    plot.bar(score_label, count, width=0.1, color=colors_2)

    plot.show()


# histogram()
bar()
