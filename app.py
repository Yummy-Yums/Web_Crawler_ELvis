import time

from crawler.Crawler import Crawler

url_1 = 'https://turntabl.io'
url_5 = 'http://www.baidu.com'
url_6 = 'https://www.youtube.com'
url_7 = 'https://community.hubspot.com'
url_8 = 'https://www.wikipedia.org/'
url_9 = 'https://developer.mozilla.org/en-US/docs/Web/API"'

crawler = Crawler()
start_time = time.time()
crawler.get_all_links(url_1)
duration = time.time() - start_time
print(f"Finished in {duration} seconds")
