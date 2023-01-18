import unittest


class TestCrawler:
    def test_update_non_related_weblinks(self):
        assert 'U' in 'Update non related weblinks'

    def test_add_weblinks(self):
        assert 'A' in 'Add weblinks'

    def test_gather_all_links_under_domain(self):
        assert 'G' in 'Gather all links under the domain'

    def test_get_all_links(self):
        assert 'G' in 'Get all links'
