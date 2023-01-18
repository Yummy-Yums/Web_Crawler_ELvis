import os.path
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
    result = thread1.get()
    thread2 = ThreadPool(2).apply_async(create_folder_for_file, (set(result),))
    thread2.get()


def decode_webpage(url: str):
    """ Decodes a webpage to be crawled """
    try:
        if urlopen(url).read():
            return urlopen(url).read().decode("utf-8")
    except UnicodeDecodeError:
        return f"Can't decode {url}"
    except MarkupResemblesLocatorWarning:
        return f"No external links found"
    except HTTPError as err:
        return err


def add_to_queue(children, queue):
    for child in children:
        queue.append(child)


# relation_dict = {'related': "'x['href']" and "x['href'].startswith('/')'",
#                  'non_related': "x['href']" and not "x['href'].startswith('/')" and "x['href'].startswith('http')"}
#
#
# def get_pages(parsed_html, option):
#     return set(map(lambda x: x['href'], filter(lambda x: f"{relation_dict[option]}", parsed_html)))


# TODO: Refactor get_related_pages and get_non_related_pages to be one
def get_related_pages(pages):
    # condition = "x['href']" and "x['href'].startswith('/')"
    return set(map(lambda x: x['href'],
                   filter(lambda x: x['href'] and x['href'].startswith('/'),
                          pages)))


def get_non_related_pages(pages):
    # condition =
    return set(map(lambda x: x['href'],
                   filter(lambda x: x['href'] and not x['href'].startswith('/') and x['href'].startswith('http'),
                          pages)))
