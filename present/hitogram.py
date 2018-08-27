import matplotlib.pyplot as plot
from analysis import score


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
    colors_2 = ['red', 'chartreuse', 'deepskyblue', 'plum', 'darkorange', 'c', 'lightskyblue', 'lime', 'cyan', 'chartreuse']

    fig, ax = plot.subplots()

    ax.set_xlabel('Rating')
    ax.set_ylabel('Number')
    ax.set_title('Book Ratings Allocation')
    plot.bar(score_label, count, width=0.7, tick_label=score_label, color=colors_2)

    plot.show()


# histogram()
bar()