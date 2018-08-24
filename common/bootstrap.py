import tools.bookspider as spider
import tools.proxyutils as pu
import tools.datahandler as dh
import time

print("Book Finder Process Start...")

bookAllHot = "https://book.douban.com/tag/?view=cloud"
bookAllTypes = "https://book.douban.com/tag/?view=type"
urlRoot = "https://book.douban.com"
doubanBookTypeFile = '/Users/cloudy/PycharmProjects/bookfinder/venv/BookTypes.txt'

# urlNovel = '/tag/小说'
BOOK_QUERY = '?start=%d&type=T'
RETRY = 3

proxies = pu.get_proxies_from_file('../tools/Proxy/Proxy 2018-06-05.txt')
proxy = pu.get_random_ip(proxies)

retry_num_type = 1

print(proxy)


typeList = spider.read_types_from_file(doubanBookTypeFile)

print("break point...")

for bookType in typeList:
    bookTypeDetail = bookType.split('|||')
    link = bookTypeDetail[2].strip()
    typename = bookTypeDetail[1].strip()
    print(link)

    index = 0
    while True:
        proxy = pu.get_random_ip(proxies)
        book_query = ''
        booksInThisPage = []
        if index != 0:
            book_query = BOOK_QUERY % (index * 20)
        try:
            booksInThisPage = spider.find_books_of_type(typename, urlRoot, link, book_query, index + 1, True, proxy)
        except Exception:
            retry_num = 1
            while retry_num <= RETRY:
                proxies.remove(proxy)
                proxy = pu.get_random_ip(proxies)
                try:
                    booksInThisPage = spider.find_books_of_type(typename, urlRoot, link, book_query, index + 1, True, proxy)
                except Exception:
                    print(Exception)
                    continue
                finally:
                    retry_num += 1
            if retry_num == 4:
                booksInThisPage = spider.find_books_of_type(typename, urlRoot, link, book_query, index + 1, True, '')

        index += 1

        if booksInThisPage.__len__() == 0:
            break

        time.sleep(2)

    dh.update_handled_type('HandledTypes.txt', bookType)

    # break  # TODO delete later
    # print(booksInThisPage)

print("Book Finder Process End...")
