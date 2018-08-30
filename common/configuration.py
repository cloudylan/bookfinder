import urllib

HTML_PARSER = 'html.parser'
dataSplitter = '|||'
db_path = '/Users/cloudy/Data/book/bookdb.sqlite3'
label_file_path = '/Users/cloudy/Data/book/bookfile/labels'
font_path = u'/Users/cloudy/Data/book/font/华文仿宋.ttf'


user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'
client_id_label = 'X-DevTools-Emulate-Network-Conditions-Client-Id'
client_id = '168EF8B869683A6149D86AAB3B5CA978'
cookie = 'random'


# SQL
get_unprocessed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS \'N\';'
update_processed_sql = "UPDATE TYPE_BOOK SET PROCESSED='%s' WHERE ID=%d"
clean_book_detail = "delete from book_detail where id not in (select min(id) from book_detail group by isbn,link)"
get_count_duplicated = "select count(*) from book_detail where link like '%s'"
select_duplicated_book_detail = "select id,name,isbn,link from book_detail where id not in (select min(id) from book_detail group by isbn,link) and isbn is not 'NA';"
get_unprocessed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS NOT \'Y\';'
get_processed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS \'Y\';'
get_book_detail_by_link = "SELECT count(*) FROM BOOK_DETAIL WHERE LINK LIKE '%s';"
delete_detail_by_link = "delete (select min(id) from book_detail where link like '%s')"


# Score SQL
# get_score_grouping = "SELECT COUNT(ID), RATINGS FROM BOOK_DETAIL GROUP BY RATINGS;"
get_score_grouping = "select count(id), ratings from (select * from book_detail where id in (select min(id) from book_detail where isbn is not 'NA' group by isbn)) group by ratings;"

# Labels SQL
get_all_labels = 'SELECT LABEL,NAME,VOTE_PEOPLE,AUTHOR,RATINGS,ISBN FROM BOOK_DETAIL ORDER BY ISBN;'
labels_group_by_isbn = "select LABEL,NAME,VOTE_PEOPLE,AUTHOR,RATINGS,ISBN from book_detail where id in (select min(id) from book_detail where isbn is not 'NA' group by isbn) order by isbn;"


def get_opener():

    opener = urllib.request.build_opener()
    opener.addheaders = {('User-agent',
                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'),
                         ('Accept',
                          'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
                         ('Cookie',
                          ''),
                         ('Upgrade-Insecure-Requests', '1'),
                         ('Cache-Control', 'no-cache')
                         }
    return opener
