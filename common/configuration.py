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
get_unprocessed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS NOT \'Y\';'
update_processed_sql = "UPDATE TYPE_BOOK SET PROCESSED='%s' WHERE ID=%d"
clean_book_detail = "delete from book_detail where id not in (select min(id) from book_detail group by isbn,link)"
get_count_duplicated = "select count(*) from book_detail where link like '%s'"
select_duplicated_book_detail = "select id,name,isbn,link from book_detail where id not in (select min(id) from book_detail group by isbn,link) and isbn is not 'NA';"
get_unprocessed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS NOT \'Y\';'
get_processed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS \'Y\';'
get_book_detail_by_link = "SELECT count(*) FROM BOOK_DETAIL WHERE LINK LIKE '%s';"
delete_detail_by_link = "delete (select min(id) from book_detail where link like '%s')"


# Score SQL
get_score_grouping = "SELECT COUNT(ID), RATINGS FROM BOOK_DETAIL GROUP BY RATINGS;"

# Labels SQL
get_all_labels = 'SELECT LABEL,NAME,VOTE_PEOPLE FROM BOOK_DETAIL;'


def get_opener():

    opener = urllib.request.build_opener()
    opener.addheaders = {('User-agent',
                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'),
                         ('Accept',
                          'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
                         ('Cookie',
                          'gr_user_id=f4ea66f2-7734-428d-8395-ca5acb8aeeb0; __ads_session=CxId0cQ66ghayAQG+AA=; __yadk_uid=xOeWi2IIl8EYSdlomnavGjlTYyaD8LoA; bid=bBVYOIpVLWA; _ga=GA1.2.1481930542.1457838662; _vwo_uuid_v2=7949DC5648B4EDA94CD30BFE660C3C0E|f4700311195db3ff0d14f6edf750c90f; __utmc=30149280; __utmv=30149280.7370; __utmc=81379588; ue="cloudylan@126.com"; push_noty_num=0; push_doumail_num=0; ll="118124"; douban-profile-remind=1; ap=1; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1532973744; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1532973744; ct=y; douban-fav-remind=1; viewed="6524140_3719247_21319773_26370384_27006492_26963321_20424526_25779298_25985021_27148613"; ps=y; __utmz=30149280.1535197997.100.57.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; dbcl2="73709635:n2pS+GNl1hs"; ck=3yN6; __utma=30149280.1481930542.1457838662.1535337279.1535352329.104; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=bc01c1d6-38d2-459a-ad58-226e45cea656; gr_cs1_bc01c1d6-38d2-459a-ad58-226e45cea656=user_id%3A1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1535352346%2C%22https%3A%2F%2Fwww.douban.com%2Fmisc%2Fsorry%3Foriginal-url%3Dhttps%253A%252F%252Fbook.douban.com%252Fsubject%252F4238362%252F%22%5D; _pk_ses.100001.3ac3=*; __utma=81379588.272989641.1511358871.1535337371.1535352346.49; __utmz=81379588.1535352346.49.21.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/misc/sorry; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_bc01c1d6-38d2-459a-ad58-226e45cea656=true; _pk_id.100001.3ac3=77fc349c1c9e1fa2.1511358870.49.1535352382.1535338283.; __utmb=30149280.5.10.1535352329; __utmb=81379588.3.10.1535352346'),
                         ('Upgrade-Insecure-Requests', '1'),
                         ('Cache-Control', 'no-cache')
                         }
    return opener
