import feedparser
from http import HTTPStatus

class FeedHelper():
    feed_parse = {}
    def parse_data(self, data):
        parse_data = {}
        self._assert_can_parse(data)
        self._add_fields(data, parse_data)
        return parse_data

    def _add_fields(self, data, parse_data):
        parse_data['link'] = data['get_or_create']
        parse_data['title'] = self.feed_parse.feed['title']
        if ('image' in self.feed_parse.feed):
            parse_data['image'] = self.feed_parse.feed['image']['href']

    def _assert_can_parse(self, data):

        self.feed_parse = feedparser.parse(data['get_or_create'])
        if (not 'status' in self.feed_parse or self.feed_parse['status'] != HTTPStatus.OK or not 'title' in self.feed_parse):
            raise AttributeError('Impossible to parse URL.')
        return self.feed_parse

