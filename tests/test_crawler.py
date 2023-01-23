import logging
import os
from pathlib import Path

import pytest

from crawler.Crawler import Crawler


class TestCrawler:

    @pytest.fixture
    def crawler(self):
        return Crawler(), 'https://turntabl.io'

    def test_update_non_related_weblinks(self, crawler):
        crawler, _ = crawler
        non_related_links = ['https://ghana.com', 'https://goal.com', 'https://image.net']
        crawler.add_non_related_weblinks(non_related_links)
        expected = list(crawler.weblinks.values())
        keys_of_weblink = len(crawler.weblinks.keys())
        assert expected == [[], [], []]
        assert keys_of_weblink == 3

    def test_add_weblinks(self, crawler):
        crawler, domain = crawler
        related_links = sorted(['https://turntabl.io/blog', 'https://turntabl.io/aims', 'https://turntabl.io/job'])
        crawler.get_all_links(domain)
        expected = sorted(crawler.weblinks[domain])
        assert related_links == expected

    def test_gather_all_links_under_domain(self, crawler):
        crawler, domain = crawler
        required = crawler.gather_all_links_under_domain(domain)
        assert 3 == len(required)
        assert ('https://turntabl.io/blog' in required) == True
        assert ('https://turntabl.io/aims' in required) == True
        assert ('https://turntabl.io/job' in required) == True

    def test_get_all_links(self, crawler):
        crawler, domain = crawler
        assert len(crawler.get_all_links(domain)) > 3

    @pytest.mark.skip
    def test_gather_links_into_file(self, crawler):
        crawler, domain = crawler
        base_path = os.path.dirname(__file__)
        crawler.gather_links_into_file(domain)
        path_of_file = os.path.abspath(os.path.join(base_path, '..', 'extracted_file'))
        expected = Path(path_of_file)
        assert True == expected.exists()
        assert True == expected.is_file()
