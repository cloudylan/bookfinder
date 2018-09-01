import os
import io

folder_path = '/Users/cloudy/PycharmProjects/bookfinder/venv/book_by_types'

print('List all files in data folder:')

files = []

index = 0
for (root, sub_folders, file_names) in os.walk(folder_path):
    print(++ index)
    print(root)
    for filename in file_names:
        file = os.path.join(root, filename)
        files.append(file)

print('%d files are found' % (files.__len__()))

for file in files:
    print(file + ' is processing.')
    book_data = io.open(file, 'r')
    books = book_data.readlines()
    book_data.close()
    count = books.__len__()

    print(count)
    processed = 0
    for book in books:
        print(book)
        processed = processed + 1

    # if processed == count:
    #     os.rename(file, (file+'_Done'))
    # else:
    #     os.rename(file, (file+'_%d_left' % (count - processed)))
    
    # processing spider

    break

print('Process end.')
