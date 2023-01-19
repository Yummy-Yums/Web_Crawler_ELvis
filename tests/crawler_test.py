import unittest

import pytest

from crawler.Crawler import Crawler


class TestCrawler:
    def test_update_non_related_weblinks(self):
        crawler = Crawler()
        non_related_links = ['https://ghana.com', 'https://goal.com', 'https://image.net']
        crawler.add_non_related_weblinks(non_related_links)
        expected = list(crawler.weblinks.values())
        keys_of_weblink = len(crawler.weblinks.keys())
        assert [[], [], []] == expected
        assert 3 == keys_of_weblink

    def test_add_weblinks(self):
        crawler = Crawler()
        domain = 'https://turntabl.io'
        related_links = sorted(['https://turntabl.io/blog', 'https://turntabl.io/aims', 'https://turntabl.io/job'])
        crawler.get_all_links(domain)
        expected = sorted(crawler.weblinks[domain])
        assert expected == related_links

    @pytest.mark.skip
    def test_gather_all_links_under_domain(self):
        assert 'G' in 'Gather all links under the domain'

    @pytest.mark.skip
    def test_get_all_links(self):
        assert 'G' in 'Get all links'

    @pytest.mark.skip
    def test_gather_links_into_file(self):
        assert 'G' in 'Get all links'
