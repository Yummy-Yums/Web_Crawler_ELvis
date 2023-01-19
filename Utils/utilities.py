import os.path
from http.client import RemoteDisconnected
from multiprocessing.pool import ThreadPool
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import MarkupResemblesLocatorWarning


def create_file(data):
    path = os.path.join(os.pardir, 'extracted_file')
    with open(path, 'w') as fb:
        for link in data:
            fb.write(link + '\n')
    print('\n******** Done with extraction ******** ')


def create_folder_for_file(data):
    """ Generate a file with all the links gathered """
    base_path = os.path.dirname(__file__)
    new_file = os.path.abspath(os.path.join(base_path, '..', 'extracted_file'))
    if os.path.exists(new_file):
        os.remove(new_file)
        return create_file(data)
    return create_file(data)


def combine_dictionary_keys_and_values(dictionary_links, all_links):
    for key, value in dictionary_links.items():
        all_links.add(key)
        if len(value):
            for link in value:
                all_links.add(link)
    return all_links


def extract_all_web_links(dictionary_of_links: dict):
    """ Gathers a dictionary of links into a set """
    final_list_of_links = set()
    thread1 = ThreadPool(1).apply_async(combine_dictionary_keys_and_values, (dictionary_of_links, final_list_of_links,))
    return set(thread1.get())


def decode_webpage(url: str):
    """ Decodes a webpage to be crawled """
    try:
        return urlopen(url)
    except (
            UnicodeDecodeError, HTTPError, MarkupResemblesLocatorWarning, RemoteDisconnected,
            RemoteDisconnected) as err:
        return err


def add_to_visited_links(children, queue):
    for child in children:
        queue.append(child)
    return queue


# relation_dict = {'related': "'x['href']" and "x['href'].startswith('/')'",
#                  'non_related': "x['href']" and not "x['href'].startswith('/')" and "x['href'].startswith('http')"}
#
#
# def get_pages(parsed_html, option):
#     return set(map(lambda x: x['href'], filter(lambda x: f"{relation_dict[option]}", parsed_html)))


# TODO: Refactor get_related_pages and get_non_related_pages to be one
def get_pages(url, option):
    my_result = None
    match option:
        case 'related':
            my_result = filter(lambda x: x['href'] and x['href'].startswith('/'), url)
        case 'non_related':
            my_result = filter(lambda x: x['href']
                                         and not x['href'].startswith('/')
                                         and x['href'].startswith('http'), url)
    return set(map(lambda x: x['href'], my_result))
