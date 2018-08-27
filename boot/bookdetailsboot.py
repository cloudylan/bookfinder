from spiders import bookspider as spider
import sqlite3
from common import configuration as config
import model.book as book
import traceback


local_html = '/Users/cloudy/Dev/git/bookfinder/test/Beyond Nature and Culture (豆瓣).html'
local_html2 = '/Users/cloudy/Dev/git/bookfinder/test/超凡領袖的挫敗 (豆瓣).html'
local_html3 = '/Users/cloudy/Dev/git/bookfinder/test/外教社·朗文小学英语分级阅读1 (豆瓣).html'
get_unprocessed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS NOT \'Y\';'
update_processed_sql = "UPDATE TYPE_BOOK SET PROCESSED='%s' WHERE ID=%d"
test_case = [local_html]
header = 'NAME|||' + 'AUTHOR|||' + 'PUBLISHER|||' + 'ISBN|||' + 'SUB_TITLE|||' + 'YEAR|||' + 'PAGE_NUMBER|||' + 'PRICE|||' + 'STYLE|||' + \
         'SERIALS|||' + 'ORIGIN_NAME|||' + 'RATING|||COMMENT_POPULATION|||STAR5|||STAR4|||STAR3|||STAR2|||STAR1|||LABEL|||PICTURE'
print(header)


# for test in test_case:
#     status = spider.get_single_book_details(test, False, True)
#     print(status)

conn = sqlite3.connect(config.db_path)
cursor = conn.execute(get_unprocessed_sql)
unprocessed_books = []

for data in cursor:
    text = config.dataSplitter.join([str(data[0]), data[1].strip(), data[2].strip(), data[3].strip(), 'NA', str(data[5]).strip()])
    booklink = book.BookLink(text)
    booklink.id = data[0]
    unprocessed_books.append(booklink)
cursor.close()

print(unprocessed_books.__len__())


for book_link in unprocessed_books:
    status = 'N'
    try:
        status = spider.get_single_book_details(book_link.link, True, False)
        print('===' + status + '::' + book_link.link)

    except Exception as e:
        print(e)
        traceback.print_exc()
        if '403: Forbidden' in e.__str__():
            break
        continue

    if status is 'Y':
        conn.execute(update_processed_sql % (status, book_link.id))
        conn.commit()
