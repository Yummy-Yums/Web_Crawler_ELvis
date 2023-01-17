import os.path
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import MarkupResemblesLocatorWarning


def create_folder_for_file(data):
    path = os.path.join(os.pardir, 'extracted_file')
    with open(path, 'x') as fb:
        for link in data:
            fb.writelines(link + '\n')


def extract_all_web_links(dictionary_of_links):
    final_list_of_links = set()
    for k, v in dictionary_of_links.items():
        final_list_of_links.add(k)
        if len(v):
            for item in v:
                final_list_of_links.add(item)
    create_folder_for_file(final_list_of_links)


def decode_webpage(url):
    try:
        if urlopen(url).read():
            return urlopen(url).read().decode("utf-8")
    except UnicodeDecodeError:
        return f"Can't decode {url}"
    except MarkupResemblesLocatorWarning:
        return f"No external links found"
    except HTTPError as err:
        return err
