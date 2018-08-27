import sqlite3
from common import configuration as config
from tools import datahandler as handler

vote_number_limit = 200


def prepare_file_all_labels():
    conn = sqlite3.connect(config.db_path)
    cursor = conn.execute(config.get_all_labels)

    label_text = ''
    name_text = ''

    for item in cursor:
        if item[2] > vote_number_limit:
            label_text = label_text + item[0] + ','
        name_text = name_text + item[1] + ','

    handler.save_to_file(config.label_file_path, 'Labels', label_text)
    handler.save_to_file(config.label_file_path, 'Names', name_text)


prepare_file_all_labels()
