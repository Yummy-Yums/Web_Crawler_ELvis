import re
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool

from bs4 import BeautifulSoup

from crawler.Utils.utilities import extract_all_web_links, decode_webpage, get_related_pages, get_non_related_pages, \
    add_to_queue


class Crawler:
    def __init__(self):
        self.weblinks = dict()

    def _update_weblinks(self, links):
        """ For links not related to the domain, their values in the dictionary is [] """
        for link in links:
            self.weblinks[link] = []

    def _add_weblink(self, link, update):
        """ Adding links related to the domain to the weblinks dictionary """
        self.weblinks[link] = update

    def _gather_all_links_under_domain(self, input_url):
        """ Gathering all the weblinks """
        print('Gathering all links...')
        parser = 'html.parser'
        response = decode_webpage(input_url)
        soup = BeautifulSoup(response, parser)

        thread1 = ThreadPool(2).apply_async(get_related_pages, (soup.find_all('a', href=True),))
        thread2 = ThreadPool(1).apply_async(get_non_related_pages, (soup.find_all('a', href=True),))
        related_links = thread1.get()
        non_related_links = thread2.get()

        with ThreadPoolExecutor(2) as executor:
            executor.submit(self._update_weblinks, non_related_links)

        with ThreadPoolExecutor(1) as executor:
            executor.submit(get_non_related_pages, (soup.find_all('a', href=True),))

        print('Active threads:', threading.activeCount())
        print('Number of web_links:', len(self.weblinks) + 1)

        all_related_pages = map(lambda x: input_url + x if re.match('/+', x) else x, related_links)
        return set(filter(lambda x: x[:-1] != input_url, all_related_pages))

    def get_all_links(self, url) -> None:
        """ Uses depth-first-search(DFS) algorithm to gather the links  """
        my_queue = deque()
        my_queue.append(url)
        while my_queue:
            current_link = my_queue.pop()
            if self._gather_all_links_under_domain(current_link):
                self._add_weblink(current_link, self._gather_all_links_under_domain(current_link))

                # self.add_to_queue(self._gather_all_links_under_domain(current_link), my_queue)
                t4 = ThreadPool(6).apply_async(add_to_queue,
                                               (self._gather_all_links_under_domain(current_link), my_queue,))
                t4.get()
            else:
                self._add_weblink(current_link, [])

        return extract_all_web_links(self.weblinks)
