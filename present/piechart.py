import matplotlib.pyplot as plot
from analysis import score


def pie():
    allocations = score.score_allocation()
    to_present = []
    other = score.Allocation('Others', 0)

    for allo in allocations:
        if allo.count > 100:
            to_present.append(allo)
        else:
            other.count = other.count + allo.count

    to_present.append(other)

    count = [item.count for item in to_present]
    score_label = [item.label for item in to_present]
    explode = [0 for i in range(count.__len__())]
    explode[0] = 1.0

    plot.pie(count, explode=explode, labels=score_label, autopct='%1.1f%%', shadow='False', startangle=90)

    plot.axis('equal')
    plot.show()

    print(count)
    print(score_label)


pie()


