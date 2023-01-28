import logging
import re
import threading
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from collections import deque

from crawler import *


class Crawler:
    __slots__ = ['weblinks']
    def __init__(self):
        self.weblinks = dict()

    def add_non_related_links_to_weblinks(self, links):
        """ Add non-related links with values=[] to the weblinks dictionary  """
        for link in links:
            self.weblinks[link] = []

    def add_related_weblinks(self, link, update):
        """ Add related links to the weblinks dictionary """
        self.weblinks[link] = update

    def gather_all_weblinks(self, input_url):
        """ Gathering all the weblinks """
        response = decode_webpage(input_url).read().decode("utf-8")
        soup = BeautifulSoup(response, 'html.parser')

        thread_pool_1 = ThreadPool(3).apply_async(get_pages, (soup.find_all('a', href=True), 'related',))
        thread_pool_2 = ThreadPool(1).apply_async(get_pages, (soup.find_all('a', href=True), 'non_related',))
        related_links = thread_pool_1.get()
        non_related_links = thread_pool_2.get()

        with ThreadPoolExecutor(max_workers=1) as executor:
            executor.submit(self.add_non_related_links_to_weblinks, non_related_links)

        # For debugging purposes
        # logging.log(msg=f'Active threads:{threading.activeCount()}', level=logging.WARN)
        # logging.log(msg=f'Number of web_links:{len(self.weblinks) + 1}', level=logging.WARN)

        all_related_pages = map(lambda link: input_url + link if re.match('/+', link) else link, related_links)
        return set(filter(lambda x: x[:-1] != input_url, all_related_pages))

    def get_all_links(self, url) -> None:
        print('Gathering all links...')
        """ Uses depth-first-search(DFS) algorithm to gather the links  """
        visited_links = [url]
        while visited_links:
            current_link = visited_links.pop()
            if current_link not in self.weblinks and self.gather_all_weblinks(current_link):
                self.add_related_weblinks(current_link, self.gather_all_weblinks(current_link))

                t4 = ThreadPool(3).apply_async(add_to_visited_links,
                                               (self.gather_all_weblinks(current_link), visited_links,))
                t4.get()
            elif current_link not in self.weblinks:
                self.add_related_weblinks(current_link, [])
        return extract_all_web_links(self.weblinks)

    def gather_links_into_file(self, input_url):
        """ Calls the function that creates a file for storing the results  """
        self.get_all_links(input_url)
        return create_file_for_storing_results(self.weblinks)
