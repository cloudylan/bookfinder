from tools import bookspider as spider
import sqlite3
from common import configuration as config
import model.book as book


local_html = '/Users/cloudy/Dev/git/bookfinder/test/singlebook.html'
local_html2 = '/Users/cloudy/Dev/git/bookfinder/test/谜样的三毛世界 (豆瓣).html'
local_html3 = '/Users/cloudy/Dev/git/bookfinder/test/条目不存在.html'
get_unprocessed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS NOT \'Y\';'
update_processed_sql = "UPDATE TYPE_BOOK SET PROCESSED='%s' WHERE ID=%d"
test_case = [local_html2, local_html3]
header = 'NAME|||' + 'AUTHOR|||' + 'PUBLISHER|||' + 'ISBN|||' + 'SUB_TITLE|||' + 'YEAR|||' + 'PAGE_NUMBER|||' + 'PRICE|||' + 'STYLE|||' + \
         'SERIALS|||' + 'ORIGIN_NAME|||' + 'RATING|||COMMENT_POPULATION|||STAR5|||STAR4|||STAR3|||STAR2|||STAR1|||LABEL|||PICTURE'
print(header)


# for test in test_case:
#     spider.get_single_book_details(test, False)


# print(get_unprocessed_sql)
#
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
    status = 'Y'
    try:
        status = spider.get_single_book_details(book_link.link, True)
    except Exception as e:
        print(e)
        continue
    conn.execute(update_processed_sql % (status, book_link.id))
    conn.commit()
