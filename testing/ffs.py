import json
import urllib.error
import urllib.parse
import urllib.request

from .api import API, Article, Articles

class FFSAPI(API):

    def query(self, rics, topics, start_date, end_date):
        params = {
            'startTime': start_date,
            'endTime': end_date,
            'ric': ','.join(map(lambda ric: 'RIC_' + ric, rics)),
            'topicCode': ','.join(topics)
        }

        encoded = []
        for key, value in params.items():
            encoded.append(key + '=' + urllib.parse.quote(value))


        url = 'http://138.68.255.10/api/newsdata?' + '&'.join(encoded)

        try:
            with urllib.request.urlopen(url) as conn:
                raw = conn.read()
        except urllib.error.HTTPError as error:
            with error:
                raw = error.read().decode()

        data = json.loads(raw)

        if not data['logfile']['success']: # something failed
            return Articles(False, error = data['error'])

        article_list = data['NewsDataSet']
        articles = []

        for article in article_list:
            rics = article['InstrumentIDs']
            topics = article['TopicCode']
            timestamp = article['TimeStamp']
            headline = article['Headline']
            body = article['NewsText']
            articles.append(Article(rics, topics, timestamp, headline, body))

        return Articles(True, articles = articles, time = data['logfile']['info']['elapsed'])