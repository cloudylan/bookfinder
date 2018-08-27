import urllib.request as req
import urllib.parse
from model.book import BookLink
from bs4 import BeautifulSoup
import datetime
import io
import tools.proxyutils as pu
import re
from tools import datahandler
from common import configuration as config

HTML_PARSER = 'html.parser'
BOOK_NUMBER_PER_PAGE = 20
RETRY = 3


def read_types_from_file(file_name):
    file = io.open(file_name, 'r')
    my_types = file.readlines()

    return my_types


def find_book_types(type_url, is_data_write, proxy):
    # print("Function: find_book_types starts.")

    type_list = []

    if proxy:
        print("using proxy %s" % proxy)
        proxy_handler = req.ProxyHandler({"http": proxy})
        opener = req.build_opener(proxy_handler)
    else:
        opener = req.build_opener()

    opener.addheaders = {('User-agent', 'Mozilla/5.0')}
    req.install_opener(opener)

    response = req.urlopen(type_url)

    soup = BeautifulSoup(response, HTML_PARSER)

    book_table = soup.find_all('table', class_='tagCol')

    if book_table.__len__() == 0:
        return type_list

    tag_links = book_table[0].find_all('a')

    type_count = 0
    for link in tag_links:
        type_count += 1
        data = str(type_count) + config.dataSplitter + link.text + config.dataSplitter + link['href'] + '\n'
        type_list.append(data)

    if is_data_write:
        book_type_file = open('BookTypes.txt', 'w')
        book_type_file.writelines(type_list)
        book_type_file.close()

    print(str(type_count) + " type(s) of book processed.")
    # print("Function: find_book_types ends.")
    return type_list


def find_books_of_type(type_name, host, url, query, page, is_write_to_file, proxy):
    print("Function: find_books_of_type starts.")

    book_list = []

    quoted_url = host + urllib.parse.quote(url)
    if query:
        quoted_url += query

    if proxy:
        proxy_handler = urllib.request.ProxyHandler({"http": proxy})
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()

    opener.addheaders = {('User-agent', 'Mozilla/5.0')}
    urllib.request.install_opener(opener)
    response = urllib.request.urlopen(quoted_url)

    soup = BeautifulSoup(response, HTML_PARSER)
    books = soup.find_all('div', class_='info')

    count = 1
    for book in books:
        name = book.a.text.strip()
        if ':' in name:
            index = name.find(':')
            name = name[0:index].strip()

        author = book.find('div', class_='pub').text.strip().split('/')[0].strip()

        book_list.append(BookLink(name, book.a['href'], author))

    if is_write_to_file:
        book_file = open('%s.txt' % (type_name + str(datetime.datetime.now())[:10]), 'a')
        for book in book_list:
            book_file.writelines(str((
                                             page - 1) * 20 + count) + config.dataSplitter + book.name + config.dataSplitter + book.author + config.dataSplitter + book.link + '\n')
            count += 1
        book_file.close()

    print("Page %d processed, %d books found." % (page, book_list.__len__()))
    print("Function: find_books_of_type ends.")
    return book_list


def get_book_types(book_all_hot, proxies, proxy):
    retry_num_type = 1
    type_list = []
    try:
        type_list = find_book_types(book_all_hot, False, proxy)
        print(type_list)
    except:
        proxies.remove(proxy)
        while retry_num_type <= RETRY:
            proxy = pu.get_random_ip(proxies)
            try:
                type_list = find_book_types(book_all_hot, False, proxy)
            except:
                continue
            finally:
                retry_num_type += 1

    if retry_num_type == 4:
        type_list = find_book_types(book_all_hot, False, '')

    return type_list


def get_single_book_details(quoted_url, write_to_file, debug):

    print('Processing ' + quoted_url)

    # proxies = pu.get_proxies_from_file('../tools/Proxy/Proxy 2018-08-21.txt')
    # proxy = pu.get_random_ip(proxies)
    #
    # print("using proxy %s" % proxy)
    # proxy_handler = req.ProxyHandler({"http": proxy})
    # opener = req.build_opener(proxy_handler)

    urllib.request.install_opener(config.get_opener())

    if debug:
        response = io.open(quoted_url, 'r')
    else:
        response = urllib.request.urlopen(quoted_url)

    bs = BeautifulSoup(response, HTML_PARSER)

    book_base = bs.find('div', id='info')
    # print(bs)

    book_exist = bs.find('span', property='v:itemreviewed')
    if book_exist is None:
        return 'NOT FOUND'

    book_name = book_exist.get_text().strip()

    # Basic data
    base_data = book_base.get_text().split()
    # print(base_data)
    page_number = 'NA'
    price = 'NA'
    isbn = 'NA'
    sub_title = 'NA'
    publisher = 'NA'
    origin_name = 'NA'
    year = 'NA'
    style = 'NA'
    serials = 'NA'

    base_spans = book_base.find_all('span', class_='pl')

    author_span = base_spans[0]
    author = 'NA'
    if u'作者' in author_span.get_text():
        author = author_span.next_sibling.next_sibling.get_text().strip().replace(' ', '').replace('\n', '')

    for span in base_spans:
        # print(span.get_text())
        if span.get_text().strip() == u'出版社:':
            publisher = span.next_sibling.strip()
        elif span.get_text().strip() == u'副标题:':
            sub_title = span.next_sibling.strip()
        elif span.get_text().strip() == u'原作名:':
            origin_name = span.next_sibling.strip()
        elif span.get_text().strip() == u'出版年:':
            year = span.next_sibling.strip()
        elif span.get_text().strip() == u'页数:':
            page_number = span.next_sibling.strip()
        elif span.get_text().strip() == u'定价:':
            price = span.next_sibling.strip()
        elif span.get_text().strip() == u'装帧:':
            style = span.next_sibling.strip()
        elif span.get_text().strip() == u'丛书:':
            serials = span.next_sibling.next_sibling.get_text()
        elif span.get_text().strip() == u'ISBN:':
            isbn = span.next_sibling.strip()

    if publisher is None or publisher is '':
        publisher = 'NA'

    complete_data = book_name + config.dataSplitter + author + config.dataSplitter + publisher + config.dataSplitter + \
                    isbn + config.dataSplitter + sub_title + config.dataSplitter + year + config.dataSplitter + page_number + config.dataSplitter + price + \
                    config.dataSplitter + style + config.dataSplitter + serials + config.dataSplitter + origin_name

    # Score
    score_section = bs.find('div', class_='rating_wrap clearbox')
    if score_section is not None:
        score_details = score_section.get_text().strip().split()
        score = score_details[1]
        if u'评价' in score:
            score = '0'
        # print(score_details.__len__())
        # print(score_details)

        number, star5, star4, star3, star2, star1 = ['0', '0', '0', '0', '0', '0']

        for index in range(score_details.__len__()):
            if u'5星' in score_details[index]:
                star5 = re.search(r'[\d]+', score_details[index + 1], flags=0).group()
            elif u'4星' in score_details[index]:
                star4 = re.search(r'[\d]+', score_details[index + 1], flags=0).group()
            elif u'3星' in score_details[index]:
                star3 = re.search(r'[\d]+', score_details[index + 1], flags=0).group()
            elif u'2星' in score_details[index]:
                star2 = re.search(r'[\d]+', score_details[index + 1], flags=0).group()
            elif u'1星' in score_details[index]:
                star1 = re.search(r'[\d]+', score_details[index + 1], flags=0).group()
            elif u'人评价' in score_details[index] and u'不足' not in score_details[index] \
                    and u'目前无人' not in score_details[index]:
                number = re.search(r'[\d]+', score_details[index], flags=0).group()

    else:
        number, star5, star4, star3, star2, star1, score = ['0', '0', '0', '0', '0', '0', '0']
    score_text = score + config.dataSplitter + number + config.dataSplitter + star5 + config.dataSplitter + star4 + \
                 config.dataSplitter + star3 + config.dataSplitter + star2 + config.dataSplitter + star1 + \
                 config.dataSplitter + quoted_url

    # Label
    label_section = bs.find('div', id='db-tags-section')
    if label_section is not None:
        label_sub_section = label_section.find('div', class_='indent')
        if label_sub_section is not None:
            labels = ','.join(bs.find('div', id='db-tags-section').find('div', class_='indent').get_text().split())
        else:
            labels = 'NA'
    else:
        labels = 'NA'

    # Picture
    pic_url = bs.find('a', class_='nbg').img['src']

    complete_data = config.dataSplitter + complete_data + config.dataSplitter + score_text + config.dataSplitter + labels + config.dataSplitter + pic_url + '\n'

    # Introduction
    short_intro = bs.find('div', class_='intro')

    intro = config.dataSplitter + book_name + config.dataSplitter + isbn + config.dataSplitter + (
        'NA' if short_intro is None else short_intro.get_text().strip()) + '\n'

    # Also like
    also_like_section = bs.find('div', id='db-rec-section')
    also_like_links = []
    also_likes_txt = 'NA'
    if also_like_section is not None:
        dls = also_like_section.find_all('dl')
        for dl in dls:
            if 'clear' in dl['class']:
                continue
            also_like_links.append(dl.dd.a.get_text().strip() + '|' + dl.dd.a['href'])

            also_likes_txt = config.dataSplitter + book_name + config.dataSplitter + isbn + config.dataSplitter + ','.join(
                also_like_links) + '\n'

    # Also like EBooks
    also_like_ebook_links = []
    ebook_links_text = 'NA'
    ebooks_section = bs.find('div', id='rec-ebook-section')
    if ebooks_section is not None:
        ebooks_section_dls = bs.find('div', id='rec-ebook-section').find_all('dl')
        for dl in ebooks_section_dls:
            also_like_ebook_links.append(dl.dd.a.get_text().strip() + '|' + dl.dd.a['href'])
        ebook_links_text = ','.join(also_like_ebook_links)

    also_e_likes = config.dataSplitter + book_name + config.dataSplitter + isbn + config.dataSplitter + ebook_links_text + '\n'

    # print(complete_data)
    # print(intro)
    # print(also_likes_txt)
    # print(also_e_likes)

    bookfilepath = '/Users/cloudy/Data/book/bookfile'

    if write_to_file:
        datahandler.save_to_file(bookfilepath + '/BookDetails', 'BookDetails', complete_data)
        datahandler.save_to_file(bookfilepath + '/AlsoLikes', 'AlsoLikes', also_likes_txt)
        datahandler.save_to_file(bookfilepath + '/Also_E_Likes', 'Also_E_Likes', also_e_likes)
        datahandler.save_to_file(bookfilepath + '/Introduction', 'Introduction', intro)

    return 'Y'
