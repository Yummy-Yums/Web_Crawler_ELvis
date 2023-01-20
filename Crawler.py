import logging
import re
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup

from crawler.Utils.utilities import *


class Crawler:
    def __init__(self):
        self.weblinks = dict()

    def add_non_related_weblinks(self, links):
        """ For links not related to the domain, their values in the dictionary is [] """
        for link in links:
            self.weblinks[link] = []

    def add_related_weblinks(self, link, update):
        """ Adding links related to the domain to the weblinks dictionary """
        self.weblinks[link] = update

    def gather_all_links_under_domain(self, input_url):
        """ Gathering all the weblinks """
        print('Gathering all links...')
        response = decode_webpage(input_url).read().decode("utf-8")
        soup = BeautifulSoup(response, 'html.parser')

        thread1 = ThreadPool(1).apply_async(get_pages, (soup.find_all('a', href=True), 'related',))
        thread2 = ThreadPool(1).apply_async(get_pages, (soup.find_all('a', href=True), 'non_related',))
        related_links = thread1.get()
        non_related_links = thread2.get()

        with ThreadPoolExecutor(2) as executor:
            executor.submit(self.add_non_related_weblinks, non_related_links)

        with ThreadPoolExecutor(1) as executor:
            executor.submit(get_pages, (soup.find_all('a', href=True), 'related',))

        # For debugging purposes
        # logging.log(msg=f'Active threads:{threading.activeCount()}', level=logging.WARN)
        # logging.log(msg=f'Number of web_links:{len(self.weblinks) + 1}', level=logging.WARN)

        all_related_pages = map(lambda link: input_url + link if re.match('/+', link) else link, related_links)
        return set(filter(lambda x: x[:-1] != input_url, all_related_pages))

    def get_all_links(self, url) -> None:
        """ Uses depth-first-search(DFS) algorithm to gather the links  """
        visited_links = deque()
        visited_links.append(url)
        while visited_links:
            current_link = visited_links.pop()
            if current_link not in self.weblinks and self.gather_all_links_under_domain(current_link):
                self.add_related_weblinks(current_link, self.gather_all_links_under_domain(current_link))

                t4 = ThreadPool(3).apply_async(add_to_visited_links,
                                               (self.gather_all_links_under_domain(current_link), visited_links,))
                t4.get()
            elif current_link not in self.weblinks:
                self.add_related_weblinks(current_link, [])
        return extract_all_web_links(self.weblinks)

    def gather_links_into_file(self, input_url):
        return create_folder_for_file(self.get_all_links(input_url))
