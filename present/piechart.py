import matplotlib.pyplot as plot
from analysis import score
import math

min_limit = 200


def pie():
    allocations = score.score_allocation()
    to_present = []
    other = score.Allocation('Others', 0)
    allo_dict = {}
    for i in range(0, 11):
        allo_dict[i] = 0

    print(allo_dict)

    for allo in allocations:
        key = math.floor(allo.label)
        allo_dict[key] = allo_dict[key] + allo.count

    for key in allo_dict:
        if allo_dict[key] > min_limit:
            to_present.append(score.Allocation(str(key * 1.0), allo_dict[key]))
        else:
            other.count = other.count + allo.count

    to_present.append(other)

    count = [item.count for item in to_present]
    score_label = [item.label for item in to_present]
    explode = [0 for i in range(count.__len__())]
    explode[3] = 0.15
    # explode[5] = 0.1

    plot.pie(count, explode=explode, labels=score_label, autopct='%1.1f%%', shadow='True', startangle=30)

    plot.axis('equal')
    plot.show()

    print(count)
    print(score_label)


pie()
