import time

from crawler.Crawler import Crawler

url_1 = 'https://turntabl.io'
# url_2 = 'https://jsonplaceholder.typicode.com/todo' #TODO: Error handling
url_5 = 'http://www.baidu.com'
# url_6 = 'https://www.youtube.com'
# url_7 = 'https://community.hubspot.com'
# url_8 = 'https://www.wikipedia.org/'
# url_9 = 'https://developer.mozilla.org/en-US/docs/Web/API"'
# url_10 = 'https://www.rottentomatoes.com'


crawler = Crawler()
start_time = time.perf_counter()
crawler.get_all_links(url_1)
duration = time.perf_counter() - start_time
print(f"Finished in {duration} seconds")
