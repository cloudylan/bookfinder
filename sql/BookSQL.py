# SQL
get_unprocessed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS NOT\'Y\';'
update_processed_sql = "UPDATE TYPE_BOOK SET PROCESSED='%s' WHERE ID=%d"
clean_book_detail = "delete from book_detail where id not in (select min(id) from book_detail group by isbn,link)"
get_count_duplicated = "select count(*) from book_detail where link like '%s'"
select_duplicated_book_detail = "select id,name,isbn,link from book_detail where id not in (select min(id) from book_detail group by isbn,link) and isbn is not 'NA';"
get_processed_sql = 'SELECT * FROM TYPE_BOOK WHERE PROCESSED IS \'Y\';'
get_book_detail_by_link = "SELECT count(*) FROM BOOK_DETAIL WHERE LINK LIKE '%s';"
delete_detail_by_link = "delete (select min(id) from book_detail where link like '%s')"
check_existence = "SELECT COUNT(*) FROM TYPE_BOOK WHERE LINK LIKE '%s';"
insert_sql = "insert into type_book(NAME, AUTHOR, LINK) values('%s','%s','%s');"
insert_detail_sql = "insert into book_detail(NAME,AUTHOR,PUBLISHER,ISBN,SUB_TITLE,YEAR,PAGE_NUMBER,PRICE,STYLE,SERIES,TRANSLATOR,RATINGS,VOTE_PEOPLE,STAR5,STAR4,STAR3,STAR2,STAR1,LABEL,PICTURE,LINK) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%f','%d',%f,%f,%f,%f,%f,'%s','%s','%s')"



# Score SQL
# get_score_grouping = "SELECT COUNT(ID), RATINGS FROM BOOK_DETAIL GROUP BY RATINGS;"
get_score_grouping = "select count(id), ratings from (select * from book_detail where id in (select min(id) from book_detail where isbn is not 'NA' group by isbn)) group by ratings;"

# Labels SQL
get_all_labels = 'SELECT LABEL,NAME,VOTE_PEOPLE,AUTHOR,RATINGS,ISBN FROM BOOK_DETAIL ORDER BY ISBN;'
labels_group_by_isbn = "select LABEL,NAME,VOTE_PEOPLE,AUTHOR,RATINGS,ISBN from book_detail where id in (select min(id) from book_detail where isbn is not 'NA' group by isbn) order by isbn;"
