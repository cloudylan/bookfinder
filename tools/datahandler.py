import io
import os
import datetime

file_path = '/Users/cloudy/PycharmProjects/bookfinder/venv/book_by_types/'
file_1 = '中国2018-06-11.txt'


def update_handled_type(file, content):
    file = io.open(file, 'a')
    file.write(content)


def join_file_path(path, files):
    file_paths = []
    for file in files:
        file_paths.append(path + file)
    return file_paths


def join_file_path_single(path, file):
    return path + file


def list_files_under(path):
    file_names = []
    for (root, dirs, files) in os.walk(path):
        file_names = files
        break

    file_paths = [join_file_path_single(path, file) for file in file_names]

    return file_paths


def save_to_file(path, file_name, text):
    book_intro = open(path + '/%s.txt' % (file_name + '-' + str(datetime.datetime.now())[:10]), 'a')
    book_intro.writelines(text)
    book_intro.close()

