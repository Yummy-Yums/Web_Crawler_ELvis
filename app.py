from crawler.Utils import *
from crawler.Crawler import Crawler
from crawler.CommandlineArgs import *

crawler = Crawler()
url = get_args().url


@timing
def run():
    if validate_url(url):
        return crawler.gather_links_into_file(url)
    print(f'Kindly check your url: {url}\n')
    return


run()
