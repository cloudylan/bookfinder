import sqlite3
from config import configuration as config
from tools import datahandler as handler

vote_number_limit = 1000
rating_limit = 8.8


def prepare_file_all_labels():
    conn = sqlite3.connect(config.db_path)
    cursor = conn.execute(config.labels_group_by_isbn)

    label_text = ''
    name_text = ''
    author_text = ''

    i = 0
    for item in cursor:

        if item[4] > 8.8:
            i = i + 1
            print(item[4])
            label_text = label_text + item[0] + ','
            author_text = author_text + item[3] + ','
            name_text = name_text + item[1] + ','

    print(i)
    handler.save_to_file(config.label_file_path, 'Labels', label_text)
    handler.save_to_file(config.label_file_path, 'Names', name_text)
    handler.save_to_file(config.label_file_path, 'Authors', author_text)


prepare_file_all_labels()
