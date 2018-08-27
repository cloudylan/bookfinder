import jieba
import wordcloud as wc
from common import configuration as config
from matplotlib import pyplot as plot


label_file = 'Labels-2018-08-27.txt'
name_file = 'Names-2018-08-27.txt'
LABEL_STOPWORDS = [u"中国", u"管理", u"社会学", u"美国", u"日本", u"文学"]
NAME_STOPWORDS = [u'The']


def jieba_word_cloud_labels():
    print("JIEBA World Cloud.")
    text = open(config.label_file_path + '/' + label_file).read()
    word_list = jieba.cut(text, cut_all=False)
    prepared = ' '.join(word_list)

    word_cloud = wc.WordCloud(background_color='white', font_path=config.font_path, max_words=20, stopwords=LABEL_STOPWORDS,
                              max_font_size=100, random_state=20).generate(prepared)

    plot.imshow(word_cloud)
    plot.axis('off')
    plot.show()


def jieba_word_cloud_names():
    print("JIEBA World Cloud.")
    text = open(config.label_file_path + '/' + name_file).read()
    word_list = jieba.cut(text, cut_all=False)
    prepared = ' '.join(word_list)

    word_cloud = wc.WordCloud(background_color='white', font_path=config.font_path, max_words=30, stopwords=NAME_STOPWORDS,
                              max_font_size=100, random_state=30).generate(prepared)

    plot.imshow(word_cloud)
    plot.axis('off')
    plot.show()


# jieba_word_cloud_labels()
jieba_word_cloud_names()
