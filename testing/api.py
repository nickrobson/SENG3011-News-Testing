class API(object):

    def query(self, rics, topics, start_date, end_date):
        pass

class Article(object):

    def __init__(self, rics, topics, timestamp, headline, body):
        self._rics = rics
        self._topics = topics
        self._timestamp = timestamp
        self._headline = headline
        self._body = body

    @property
    def rics(self):
        return self._rics

    @property
    def topics(self):
        return self._topics

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def headline(self):
        return self._headline

    @property
    def body(self):
        return self._body

    def __hash__(self):
        return hash(self.headline + '[]' + self.timestamp)

    def __eq__(self, other):
        return self.rics == other.rics and \
            self.topics == other.topics and \
            self.timestamp == other.timestamp and \
            self.headline == other.headline and \
            self.body == other.body

class Articles(object):

    def __init__(self, articles, time):
        self._articles = articles
        self._time = time

    @property
    def articles(self):
        return self._articles

    @property
    def time(self):
        return self._time
