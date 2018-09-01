import jieba
import wordcloud as wc
from config import configuration as config
from matplotlib import pyplot as plot

date_txt = '-2018-08-29.txt'
label_file = 'Labels' + date_txt
name_file = 'Names' + date_txt
author_file = 'Authors' + date_txt
# LABEL_STOPWORDS = [u"中国", u"管理", u"社会学", u"美国", u"日本", u"文学"]
NAME_STOPWORDS = [u'The']
LABEL_STOPWORDS = []
# AUTHOR_STOPWORDS = ['NA']
AUTHOR_STOPWORDS = [u'加拿大', u'古希腊', u'爱尔兰', u'译注', u'奥地利', u'主编', u'瑞士', 'NA', u'瑞典', u'哥伦比亚', u'马丁 乔治', u'编著', u'出版社', u'印度', u'选注', u'原著', u'阿根廷']


def jieba_word_cloud_labels():
    print("JIEBA World Cloud.")
    text = open(config.label_file_path + '/' + label_file).read()
    word_list = jieba.cut(text, cut_all=False)
    prepared = ' '.join(word_list)

    word_cloud = wc.WordCloud(width=1000, height=800, background_color='white', font_path=config.font_path, max_words=40, stopwords=LABEL_STOPWORDS,
                              max_font_size=150, random_state=20).generate(prepared)

    plot.imshow(word_cloud)
    plot.axis('off')
    plot.show()


def jieba_word_cloud_names():
    print("JIEBA World Cloud.")
    text = open(config.label_file_path + '/' + name_file).read()
    word_list = jieba.cut(text, cut_all=False)
    prepared = ' '.join(word_list)

    word_cloud = wc.WordCloud(width=1000, height=800, background_color='white', font_path=config.font_path, max_words=40, stopwords=NAME_STOPWORDS,
                              max_font_size=150, random_state=30).generate(prepared)

    plot.imshow(word_cloud)
    plot.axis('off')
    plot.show()


def jieba_word_cloud_authors():
    print("JIEBA World Cloud.")
    text = open(config.label_file_path + '/' + author_file).read()
    word_list = jieba.cut(text, cut_all=False)
    prepared = ' '.join(word_list)

    word_cloud = wc.WordCloud(width=1000, height=800, background_color='white', font_path=config.font_path, max_words=40, stopwords=AUTHOR_STOPWORDS,
                              max_font_size=150, random_state=20).generate(prepared)

    plot.imshow(word_cloud)
    plot.axis('off')
    plot.show()

# jieba_word_cloud_labels()
# jieba_word_cloud_names()
jieba_word_cloud_authors()