import json

from crawler.Crawler import Crawler

url_1 = 'https://turntabl.io'
url_2 = 'https://www.google.com/search?q=add+multithreading+to+web+scraping&oq=add+multithreading+to+web+scraping&aqs=chrome..69i57j33i160l2.10436j0j7&sourceid=chrome&ie=UTF-8'
url_3 = 'https://www.pluralsight.com/guides/web-scraping-with-beautiful-soup'
url_4 = 'https://finance.yahoo.com/'

crawler = Crawler()
# TODO: Write it to a file
# crawler.get_all_links(url_1)
crawler.get_all_links(url_1)
