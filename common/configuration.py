import urllib

HTML_PARSER = 'html.parser'
dataSplitter = '|||'
db_path = '/Users/cloudy/Data/book/bookdb.sqlite3'
user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Mobile Safari/537.36'
client_id_label = 'X-DevTools-Emulate-Network-Conditions-Client-Id'
client_id = '168EF8B869683A6149D86AAB3B5CA978'
cookie = 'gr_user_id=f4ea66f2-7734-428d-8395-ca5acb8aeeb0; __ads_session=CxId0cQ66ghayAQG+AA=; __yadk_uid=xOeWi2IIl8EYSdlomnavGjlTYyaD8LoA; bid=bBVYOIpVLWA; _ga=GA1.2.1481930542.1457838662; _vwo_uuid_v2=7949DC5648B4EDA94CD30BFE660C3C0E|f4700311195db3ff0d14f6edf750c90f; __utmc=30149280; __utmv=30149280.7370; __utmc=81379588; ue="cloudylan@126.com"; push_noty_num=0; push_doumail_num=0; ll="118124"; douban-profile-remind=1; ap=1; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1532973744; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1532973744; ct=y; douban-fav-remind=1; viewed="6524140_3719247_21319773_26370384_27006492_26963321_20424526_25779298_25985021_27148613"; ps=y; __utmz=30149280.1535197997.100.57.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmz=81379588.1535198277.45.20.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=30149280.1481930542.1457838662.1535298610.1535337279.103; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1535337368%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; ap_v=1,6.0; __utma=81379588.272989641.1511358871.1535298610.1535337371.48; gr_cs1_faa1ab19-6763-41b8-a866-4d4aaa830d2c=user_id%3A0; __utmt=1; dbcl2="73709635:n2pS+GNl1hs"; ck=3yN6; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=0532ffd1-9d9f-4ffd-83a8-e213967fc441; gr_cs1_0532ffd1-9d9f-4ffd-83a8-e213967fc441=user_id%3A1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_0532ffd1-9d9f-4ffd-83a8-e213967fc441=true; __utmt_douban=1; _pk_id.100001.3ac3=77fc349c1c9e1fa2.1511358870.48.1535338269.1535298611.; __utmb=30149280.22.10.1535337279; __utmb=81379588.16.10.1535337371'


# SQL
get_unprocessed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS NOT \'Y\';'
update_processed_sql = "UPDATE TYPE_BOOK SET PROCESSED='%s' WHERE ID=%d"
clean_book_detail = "delete from book_detail where id not in (select min(id) from book_detail group by isbn,link)"
get_count_duplicated = "select count(*) from book_detail where link like '%s'"
select_duplicated_book_detail = "select id,name,isbn,link from book_detail where id not in (select min(id) from book_detail group by isbn,link) and isbn is not 'NA';"
get_unprocessed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS NOT \'Y\';'
get_processed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS \'Y\';'
get_book_detail_by_link = "SELECT count(*) FROM BOOK_DETAIL WHERE LINK LIKE '%s';"
delete_detail_by_link = "delete (select min(id) from book_detail where link like '%s')";


def get_opener():

    opener = urllib.request.build_opener()
    opener.addheaders = {('User-agent',
                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'),
                         ('Accept',
                          'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
                         ('Cookie',
                          'gr_user_id=f4ea66f2-7734-428d-8395-ca5acb8aeeb0; __ads_session=CxId0cQ66ghayAQG+AA=; __yadk_uid=xOeWi2IIl8EYSdlomnavGjlTYyaD8LoA; bid=bBVYOIpVLWA; _ga=GA1.2.1481930542.1457838662; _vwo_uuid_v2=7949DC5648B4EDA94CD30BFE660C3C0E|f4700311195db3ff0d14f6edf750c90f; __utmc=30149280; __utmv=30149280.7370; __utmc=81379588; ue="cloudylan@126.com"; push_noty_num=0; push_doumail_num=0; ll="118124"; douban-profile-remind=1; ap=1; Hm_lvt_16a14f3002af32bf3a75dfe352478639=1532973744; Hm_lpvt_16a14f3002af32bf3a75dfe352478639=1532973744; ct=y; douban-fav-remind=1; viewed="6524140_3719247_21319773_26370384_27006492_26963321_20424526_25779298_25985021_27148613"; ps=y; dbcl2="73709635:Mj7qap6yx4c"; ck=OC3g; __utmz=30149280.1535197997.100.57.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; __utmz=81379588.1535198277.45.20.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=d19bdaed-c2eb-43de-a904-48d4efef53b3; gr_cs1_d19bdaed-c2eb-43de-a904-48d4efef53b3=user_id%3A1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1535293190%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.3ac3=77fc349c1c9e1fa2.1511358870.46.1535293190.1535200218.; _pk_ses.100001.3ac3=*; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_d19bdaed-c2eb-43de-a904-48d4efef53b3=true; __utma=30149280.1481930542.1457838662.1535197997.1535293190.101; __utmt_douban=1; __utmb=30149280.1.10.1535293190; __utma=81379588.272989641.1511358871.1535198277.1535293190.46; __utmt=1; __utmb=81379588.1.10.1535293190; ap_v=1,6.0'),
                         ('Upgrade-Insecure-Requests', '1'),
                         ('Cache-Control', 'no-cache')
                         }
    return opener
