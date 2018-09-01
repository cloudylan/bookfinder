import tools.datahandler as datahandler
import urllib.request
import config.configuration as config
from bs4 import BeautifulSoup
from enum import Enum
import re
import db.datasource as source
import traceback


class SimpleSpider:
    book_link = None
    data_type = None

    def __init__(self, param_book_link, param_data_type, lock):
        self.book_link = param_book_link
        self.data_type = param_data_type
        self.lock = lock

    def get_single_book_details(self, book_link, lock):
        print('Processing ' + book_link.link)

        urllib.request.install_opener(config.get_opener())
        response = urllib.request.urlopen(book_link.link)
        bs = BeautifulSoup(response, config.HTML_PARSER)

        book_base = bs.find('div', id='info')
        # print(bs)

        book_exist = bs.find('span', property='v:itemreviewed')
        if book_exist is None:
            return 'NOT FOUND'

        book_name = book_exist.get_text().strip()

        # Basic data
        # base_data = book_base.get_text().split()
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
                     config.dataSplitter + book_link.link

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

        print(complete_data)
        # print(intro)
        # print(also_likes_txt)
        # print(also_e_likes)

        # Lock!
        lock.acquire()
        bookfilepath = '/Users/cloudy/Data/book/bookfile'

        # if write_to_file:
        datahandler.save_to_file(bookfilepath + '/BookDetails', 'BookDetails', complete_data)
        datahandler.save_to_file(bookfilepath + '/AlsoLikes', 'AlsoLikes', also_likes_txt)
        datahandler.save_to_file(bookfilepath + '/Also_E_Likes', 'Also_E_Likes', also_e_likes)
        datahandler.save_to_file(bookfilepath + '/Introduction', 'Introduction', intro)
        lock.release()

        ds = source.SqliteDataSource(config.db_path)
        ds.update(config.update_processed_sql % ('Y', book_link.id))

        print('===' + 'Y' + '::' + book_link.link)

    def go(self, task):
        if task.data_type is DataType.DETAIL:
            try:
                self.get_single_book_details(task.book_link, task.lock)
            except Exception as e:
                print('Error ' + task.book_link.link + '\n' + e)
                traceback.print_exc()


class DataType(Enum):
    DETAIL = 1
    TYPE = 2
