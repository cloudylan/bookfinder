import sqlite3
from common import configuration as config
import numpy as np


class Allocation():
    def __init__(self, label, count):
        self.label = label
        self.count = count


def score_allocation():
    print("Score Allocation.")

    conn = sqlite3.connect(config.db_path)
    cursor = conn.execute(config.get_score_grouping)
    allocations = []

    for item in cursor:
        allocations.append(Allocation(item[1], item[0]))
    cursor.close()

    count = [item.count for item in allocations]
    score_label = [item.label for item in allocations]

    print(count)
    print(score_label)

    return allocations

score_allocation()


