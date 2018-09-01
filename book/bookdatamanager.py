import tools.datahandler as datahandler
import io
import os
from model.book import *
from config import configuration as config
import re
import sql.BookSQL as sql
import db.datasource as source


def transfer_book_details_data(input_file_path, write_to_db):
    file = io.open(input_file_path, 'r')
    lines = file.readlines()
    first_row = True
    book_details = []

    for line in lines:
        # print(first_row)
        try:
            if first_row is True:
                # print('---'+line)
                first_row = False
                continue
            data = line.split(config.dataSplitter)
            book_detail = BookDetail()

            book_detail.name = data[1].strip()
            book_detail.author = data[2].strip()
            book_detail.publisher = data[3].strip()
            book_detail.isbn = data[4].strip()
            book_detail.sub_title = data[5].strip()
            book_detail.publishYear = data[6].strip()
            book_detail.pageNumber = data[7].strip()
            book_detail.price = data[8].strip()
            book_detail.style = data[9].strip()
            book_detail.series = data[10].strip()
            book_detail.translator = data[11].strip()
            book_detail.ratings = data[12].strip()
            if u'评价' in book_detail.ratings:
                book_detail.ratings = '0'
            book_detail.vote_people = data[13].strip()
            book_detail.star5 = data[14].strip()
            book_detail.star4 = data[15].strip()
            book_detail.star3 = data[16].strip()
            book_detail.star2 = data[17].strip()
            book_detail.star1 = data[18].strip()

            book_detail.link = data[19].strip()
            book_detail.label = data[20].strip()
            book_detail.picture = data[21].strip()

            book_details.append(book_detail)

        except Exception as e:
            print("Error Happened: " + str(e))
            print(str(data[1]))
            continue

    print(str(book_details.__len__()) + '=========')
    ds = source.SqliteDataSource(config.db_path)
    for book in book_details:
        print(sql.insert_detail_sql % (book.name, book.author.replace('\'', ' '), book.publisher, book.isbn, book.sub_title,
                                   book.publishYear, book.pageNumber, book.price, book.style, book.series,
                                   book.translator, float(book.ratings), int(book.vote_people), float(book.star5),
                                   float(book.star4),
                                   float(book.star3), float(book.star2), float(book.star1), book.label, book.picture,
                                   book.link))
        ds.execute(sql.insert_detail_sql % (
        book.name.replace('\'', ' '), book.author.replace('\'', ' '), book.publisher.replace('\'', ' '), book.isbn,
        book.sub_title.replace('\'', ' '),
        book.publishYear, book.pageNumber, book.price, book.style.replace('\'', ' '), book.series.replace('\'', ' '),
        book.translator.replace('\'', ' '), float(book.ratings), int(book.vote_people), float(book.star5),
        float(book.star4),
        float(book.star3), float(book.star2), float(book.star1), book.label.replace('\'', ' '), book.picture,
        book.link))

    if write_to_db:
        ds.commit()
    file.close()
    os.rename(input_file_path, input_file_path + '_done')
    print('input file path:' + input_file_path + ' : ' + str(book_details.__len__()))


def transfer_files_to_db(folder_path, write_to_db):
    file_paths = datahandler.list_files_under(folder_path)
    for f_path in file_paths:
        print(f_path + '========')
        if not f_path.endswith('.txt'):
            continue
        else:
            transfer_book_details_data(f_path, write_to_db)


def transfer_also_likes(input_file_path, write_to_db):
    file = io.open(input_file_path, 'r')
    lines = file.readlines()
    book_links = []

    print('=====' + input_file_path)
    for line in lines:
        try:
            data = line.split('|||')
            if data[3] is None:
                continue

            links = data[3].split(',')

            for link in links:
                try:
                    book_lk = link.split('|')
                    # print(book_lk)
                    blk_txt = config.dataSplitter + book_lk[0] + config.dataSplitter + 'NA' + config.dataSplitter + \
                              book_lk[1] + \
                              config.dataSplitter + 'NA' + config.dataSplitter
                    book_link = BookLink(blk_txt)
                    book_links.append(book_link)
                except Exception as e:
                    print(line)
                    datahandler.save_to_file(config.also_like_file_path, 'except.txt', line)
                    continue

        except Exception as e:
            print("Error Happened: " + str(e.__cause__))
            continue

    ds = source.SqliteDataSource(config.db_path)

    print(book_links.__len__())
    print("OK")

    map_like = {}
    for bk_lk in book_links:
        # print(check_existence % ('%'+bk_lk.link+'%'))
        result = ds.execute(sql.check_existence % ('%' + bk_lk.link + '%'))
        for ind in result:
            # print(ind[0])
            if ind[0] == 0:
                map_like[bk_lk.link] = bk_lk
    print(map_like.keys().__len__())


def build_additional_also_like_list(folder_path, write_to_db):
    file_paths = datahandler.list_files_under(folder_path)
    for f_path in file_paths:
        print(f_path + '========')
        if not f_path.endswith('.txt'):
            continue
        else:
            transfer_also_likes(f_path, write_to_db)


def clean_duplicated_book_detail():
    ds = source.SqliteDataSource(config.db_path)
    ds.execute(config.clean_book_detail)

    get_duplicated_count = ds.select(config.select_duplicated_book_detail)

    for item in get_duplicated_count:
        print(item)
    get_duplicated_count.close()


def restore_processed_book_type():
    ds = source.SqliteDataSource(config.db_path)
    cursor = ds.select(config.get_processed_sql)
    processed_books = []

    # 59287|游靜|游動的影|https://book.douban.com/subject/27041178/
    # ||N
    for data in cursor:
        text = config.dataSplitter.join(
            [str(data[0]), data[2].strip(), data[1].strip(), data[3].strip(), 'NA', str(data[5]).strip()])
        booklink = BookLink(text)
        booklink.id = data[0]
        # booklink.processed = data[5].strip()
        processed_books.append(booklink)
    cursor.close()

    need_restore = []
    need_detail_clean = []
    print(processed_books.__len__())

    for processed in processed_books:
        # print(processed.id)
        lk = processed.link
        if lk is not None and lk is not '':
            # print(link)
            link_id = re.search(r'[\d]+', lk).group()
            param_link = '%' + str(link_id) + '%'

            cursor_detail = ds.select(config.get_book_detail_by_link % param_link)

            for item in cursor_detail:
                if item[0] == 0:
                    print(str(processed.id) + ':::' + processed.name + ':::' + str(item[0]) + ':::' + processed.link)
                    need_restore.append(processed)
                elif item[0] > 1:
                    need_detail_clean.append(processed)
                    print(str(processed.id) + ':::' + processed.name + ':::' + str(item[0]) + ':::'+ processed.link + ':::' + (config.get_book_detail_by_link % param_link))

    print(need_restore.__len__())
    if need_restore.__len__() > 0:
        for to_udpate in need_restore:
            ds.execute(config.update_processed_sql % ('N', to_udpate.id))

    # print(need_detail_clean.__len__())
    # if need_detail_clean.__len__() > 0:
    #     for to_delete in need_detail_clean:
    #         conn.execute()


transfer_files_to_db(config.book_detail_file_path, True)
# build_additional_also_like_list(also_like_file_path, False)
# clean_duplicated_book_detail()
# restore_processed_book_type()
# datahandler.reset_processed_detail_files(book_detail_file_path)


def transfer_book_type_data():
    book_dict = {}

    # read from file and insert into database.
    file_paths = datahandler.list_file_under(config.type_file_path)

    duplicated = 0
    file_num = 1
    for f_path in file_paths:
        if not f_path.endswith('.txt'):
            continue
        file = io.open(f_path, 'r')
        lines = file.readlines()

        print('/// Start(' + str(file_num) + '): ' + f_path)
        file_num += 1

        for line in lines:
            book = BookLink(line)
            if book.link in book_dict.keys():
                # print("Duplicated!!!" + ':' + book.link + '|||||' + book_dict[book.link].name)
                duplicated += 1
            book_dict[book.link] = book

    print('/// Duplicated %d books.' % duplicated)

    ds = source.SqliteDataSource(config.db_path)

    for key in book_dict.keys():
        book = book_dict[key]
        ds.execute(sql.insert_sql % (book.author.replace('\'', ' '), book.name.replace('\'', ' '), book.link))

    file.close()

    print(book_dict.__len__())
    print('database opened.')

    ds.close()
