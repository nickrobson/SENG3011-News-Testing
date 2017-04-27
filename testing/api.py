class API(object):

    def query(self, rics, topics, start_date, end_date):
        pass

class Article(object):

    def __init__(self, rics, topics, timestamp, headline, body):
        self.rics = sorted(rics)
        self.topics = sorted(topics)
        self.timestamp = timestamp
        self.headline = headline
        self.body = body

    def __hash__(self):
        return hash(self.headline + '[]' + self.timestamp)

    def __eq__(self, other):
        return self.rics == other.rics and \
            self.topics == other.topics and \
            self.timestamp == other.timestamp and \
            self.headline == other.headline and \
            self.body == other.body

    def __repr__(self):
        return 'Article({}, {}, {}, {}, {})'.format(*map(repr, [self.rics, self.topics, self.timestamp, self.headline, self.body]))

class Articles(object):

    def __init__(self, success, error=None, articles=None, time=None):
        self.success = success
        self.time = time
        if success:
            self.articles = sorted(articles, key = lambda a: (a.timestamp, a.headline))
        else:
            self.error = error

    def __eq__(self, other):
        if self.success != other.success:
            return False
        if not self.success:
            return self.error == other.error
        return self.articles == other.articles and \
            self.time == other.time

    def __repr__(self):
        if not self.success:
            return 'Articles({}, error = {})'.format(repr(self.success), repr(self.error))
        return 'Articles({}, articles = {}, time = {})'.format(*map(repr, [self.success, self.articles, self.time]))
