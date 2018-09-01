import sqlite3
import config.configuration as config


vote_number_limit = 300
ratings_limit = 9.2
filter = [u'词典', u'辞典', u'工具书', u'佛经', u'童话', u'童年', u'连环画', u'医学', u'五月天', u'英语学习',
          u'三毛', u'儿童文学', u'漫画', u'基督教要义', u'中医']

get_books_sql = "select name,author,ratings,vote_people,label from book_detail where vote_people > %d and ratings=%f;"


def get_books():
    conn = sqlite3.connect(config.db_path)
    cursor = conn.execute(get_books_sql % (vote_number_limit, ratings_limit))
    books = []
    for item in cursor:
        is_filter = False
        labels = item[4].split(',')
        for label in labels:
            if label in filter:
                is_filter = True
        if not is_filter:
            books.append(item[0] + ' | ' + item[1] + ' | ' + str(item[2]) + ' | ' + str(item[3]) + ' | ' + item[4])

    for book in books:
        print(book)
    print(books.__len__())

get_books()
