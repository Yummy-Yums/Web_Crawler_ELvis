from collections import deque
import re

from bs4 import BeautifulSoup

from crawler.Utils.utilities import extract_all_web_links, decode_webpage


class Crawler:
    def __init__(self):
        self.weblinks = dict()

    def __update_weblinks(self, links):
        for link in links:
            self.weblinks[link] = []

    def __add_weblink(self, link, update):
        self.weblinks[link] = update

    def __gather_all_links_under_domain(self, input_url):
        # TODO: add comments in the function
        print('Gathering all links...')
        parser = 'html.parser'
        resp = decode_webpage(input_url)
        soup = BeautifulSoup(resp, parser)

        related_pages = set(map(lambda x: x['href'],
                                filter(lambda x: x['href'] and x['href'].startswith('/'),
                                       soup.find_all('a', href=True))))
        non_related_pages = set(map(lambda x: x['href'],
                                    filter(lambda x: x['href'] and not x['href'].startswith('/'),
                                           soup.find_all('a', href=True))))

        # TODO: In case of multi-threading, delegate on thread to do this
        self.__update_weblinks(non_related_pages)

        # TODO: In case of multi-threading, delegate on thread to do this
        all_related_pages = set(map(lambda x: input_url + x if re.match('/+', x) else x, related_pages))
        return set(filter(lambda x: x[:-1] != input_url, all_related_pages))

    def get_all_links(self, url):
        my_stack = deque()
        my_stack.append(url)
        while my_stack:
            current_link = my_stack.popleft()
            if self.__gather_all_links_under_domain(current_link):
                self.__add_weblink(current_link, self.__gather_all_links_under_domain(current_link))
                for children_link in self.__gather_all_links_under_domain(current_link):
                    my_stack.append(children_link)
            else:
                self.__add_weblink(current_link, [])

        extraction = extract_all_web_links(self.weblinks)
        if extraction:
            print('\n******** Done with extraction ******** ')
        return extraction
