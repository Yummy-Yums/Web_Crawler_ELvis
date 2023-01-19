import os
from collections import deque

import pytest
from bs4 import BeautifulSoup

from crawler.Utils.utilities import *


class TestUtils:

    @pytest.fixture
    def important_value(self):
        url = 'https://turntabl.io'
        response = decode_webpage(url).read().decode("utf-8")
        return BeautifulSoup(response, 'html.parser')

    def test_create_file(self):
        msg = 'https://turntabl.io/blog/blog\nhttps://turntabl.io/blog/blogs/2019/04/15/turntabl-connectivity.html'
        base_path = os.path.dirname(__file__)
        create_file(msg)
        required = os.path.exists(os.path.abspath(os.path.join(base_path, '..', 'extracted_file')))
        assert required == True

    def test_extract_all_web_links(self):
        web_links = {'https://www.turnabl.io': {'https://turntabl.io/blog', 'https://turntabl.io/aims',
                                                'https://turntabl.io/job'}}
        required = len({'https://www.turnabl.io', 'https://turntabl.io/blog', 'https://turntabl.io/aims',
                        'https://turntabl.io/job'})
        assert required == len(extract_all_web_links(web_links))

    def test_combine_dictionary_keys_and_values(self):
        test_dictionary = {'a': 'b', 'c': 'd'}
        test_dictionary_2 = {'a': 'b', 'c': 'b'}
        required = len(combine_dictionary_keys_and_values(test_dictionary, set()))
        required_2 = len(combine_dictionary_keys_and_values(test_dictionary_2, set()))
        expected = len({'a', 'b', 'c', 'd'})
        expected_2 = len({'a', 'b', 'c'})
        assert required == expected
        assert required_2 == expected_2

    def test_decode_webpage_valid_webpage(self):
        url = 'https://turntabl.io'
        response = decode_webpage(url)
        assert 200 == response.getcode()

    def test_decode_webpage_invalid_webpage(self):
        url = 'https://jsonplaceholder.typicode.com/todo'
        response = decode_webpage(url)
        assert 404 == response.getcode()

    def test_get_related_pages(self, important_value):
        all_pages = important_value.find_all('a', href=True)
        expected = {'/job', '/aims', '/', '/blog'}
        assert expected == get_pages(all_pages, 'related')
        assert 4 == len(get_pages(all_pages, 'related'))

    def test_get_non_related_pages(self, important_value):
        all_pages = important_value.find_all('a', href=True)
        expected = {'https://twitter.com/turntablio', 'https://github.com/turntabl',
                    'https://www.google.co.uk/maps/place/turntabl/@5.6326822,-0.2382382,19z/data=!3m1!4b1!4m13!1m7!3m6!1s0xfdf996579ca9ebd:0x99822538ef7ed82f!2sAchimota,+Ghana!3b1!8m2!3d5.612781!4d-0.234345!3m4!1s0xfdf9954d603e5b3:0xd24eb41c04c54f63!8m2!3d5.6326809!4d-0.237691'}
        assert expected == get_pages(all_pages, 'non_related')
        assert 3 == len(get_pages(all_pages, 'non_related'))

    def test_add_to_visited_links(self):
        my_queue = deque()
        my_queue.append('/job')
        my_queue.append('/aims')
        my_queue.append('/blog')
        expected = len(add_to_visited_links({'/job', '/aims', '/blog'}, deque()))

        assert 3 == expected
