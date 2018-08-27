class Book:
    id = ''
    isbn = ''
    name = ''
    author = ''


class BookComments(Book):
    score = 0
    star = 1
    star1 = 0.0
    star2 = 0.0
    star3 = 0.0
    star4 = 0.0
    star5 = 0.0
    readerNum = 0


class Comment:
    isbn = ''


class BookDetail(Book):
    publisher = ''
    originalName = ''
    translator = ''
    publishYear = ''
    sub_title = ''
    pageNumber = 0
    price = ''
    style = ''
    series = ''
    ratings = 0.0
    vote_people = 0
    star5 = 0.0
    star4 = 0.0
    star3 = 0.0
    star2 = 0.0
    star1 = 0.0
    link = ''
    picture = ''
    label = ''


class BookLink:
    id = ''

    def __init__(self, name, link, author, from_type, processed):
        self.name = name
        self.link = link
        self.author = author
        self.from_type = from_type
        self.processed = processed

    def __init__(self, text):
        if text is not None:
            data = text.split("|||")
            self.name = data[1]
            self.link = data[3]
            self.author = data[2]
            self.from_type = 'NA'
            self.processed = data[5]
