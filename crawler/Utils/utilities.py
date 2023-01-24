import os.path
import urllib
from functools import wraps
from http.client import RemoteDisconnected
from multiprocessing.pool import ThreadPool
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from time import perf_counter


def create_file_for_storing_results(data):
    """ Generate a file with all the links gathered """
    base_path = os.path.dirname(__file__)
    path = os.path.abspath(os.path.join(base_path, '..\..', 'extracted_file'))
    if os.path.exists(path):
        os.remove(path)
    with open(path, 'w') as fb:
        for link in data:
            fb.write(link + '\n')
        print('\n******** Done with extraction and file created! ******** ')


def combine_dictionary_keys_and_values(dictionary_links, all_links):
    """ A function to combine the values and keys of a dictionary as a set """
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
            UnicodeDecodeError, HTTPError, RemoteDisconnected,
            RemoteDisconnected) as err:
        return err


def add_to_visited_links(children, queue):
    """ A function to add a value to an existing queue """
    for child in children:
        queue.append(child)
    return queue


def get_pages(url, option):
    """ A function to extract links on a webpage based on the option(either related oor non_related)  """
    my_result = None
    match option:
        case 'related':
            my_result = filter(lambda x: x['href'] and x['href'].startswith('/'), url)
        case 'non_related':
            my_result = filter(lambda x: x['href']
                                         and not x['href'].startswith('/')
                                         and x['href'].startswith('http'), url)
    return set(map(lambda x: x['href'], my_result))


# TODO: Write test
def timing(f):
    """A decorator function that times the execution of the input-argument, which is also a function"""

    @wraps(f)
    def inner_function(*args, **kwargs):
        start_time = perf_counter()
        result = f(*args, **kwargs)
        duration = perf_counter() - start_time
        print(f"Finished in {duration:2.2f} seconds")
        return result

    return inner_function


def validate_url(url: str):
    """ A function to validate the url before processing and crawling the links """
    try:
        req = urllib.request.urlopen(url).getcode()
        return req == 200
    except HTTPError as e:
        return f"Error: {e.code}"
    except (ValueError, URLError) as e:
        return e
