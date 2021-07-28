import feedparser
from http import HTTPStatus

class SubscriptionFeedHelper():
    def parse_data(self, data):
        feed_parse = self._assert_can_parse(data)
        parse_data = self._select_fields(data, feed_parse)
        return parse_data

    def _select_fields(self, data,feed_parse):
        parse_data = {}
        parse_data['link'] = data['link']
        parse_data['title'] = feed_parse.feed['title']
        if('entries' in feed_parse):
            parse_data['entries'] = feed_parse['entries']
        if ('image' in feed_parse.feed):
            parse_data['image'] = feed_parse.feed['image']['href']
        return parse_data

    def _assert_can_parse(self, data):

        feed_parse = feedparser.parse(data['link'])
        if (not 'status' in feed_parse or feed_parse['status'] != HTTPStatus.OK or not 'title' in feed_parse.feed):
            raise AttributeError('Impossible to parse URL.')
        return feed_parse

