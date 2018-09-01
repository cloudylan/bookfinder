from spiders import simplespider as spider
import db.datasource as source
from config import configuration as config
import model.book as book
from threading import RLock
from concurrent.futures import ThreadPoolExecutor


local_html = '/Users/cloudy/Dev/git/bookfinder/test/Beyond Nature and Culture (豆瓣).html'
local_html2 = '/Users/cloudy/Dev/git/bookfinder/test/singlebook.html'
local_html3 = '/Users/cloudy/Dev/git/bookfinder/test/外教社·朗文小学英语分级阅读1 (豆瓣).html'
test_case = [local_html, local_html2, local_html]
lock = RLock()


def start_shadow_spidering():
    ds = source.SqliteDataSource(config.db_path)
    cursor = ds.select(config.get_unprocessed_sql)
    unprocessed_books = []

    for data in cursor:
        text = config.dataSplitter.join([str(data[0]), data[1].strip(), data[2].strip(), data[3].strip(), 'NA', str(data[5]).strip()])
        booklink = book.BookLink(text)
        booklink.id = data[0]
        unprocessed_books.append(booklink)
    cursor.close()

    print(str(unprocessed_books.__len__()) + ' unprocessed records.')

    with ThreadPoolExecutor(2) as executor:
        for each in unprocessed_books:
            task = spider.SimpleSpider(each, spider.DataType.DETAIL, lock)
            executor.submit(task.go, task)

start_shadow_spidering()
