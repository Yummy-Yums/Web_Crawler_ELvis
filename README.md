# Details
---------
Write a program which accepts an input url, and perform a web crawl on the URL, without using any external library

This entails listing all URL’s that are on the page of that URL, and then subsequently crawl those URL’s,  
until all URL’s under the supplied domain have been crawled. 
Print out the results of all URL’s however only crawl those sites which are under the domain of that url.
e.g. if we crawl https://turntabl.io then we should list https://twitter.com/turntablio as it’s on that page, 
however we shouldn’t crawl it. We will list and crawl https://turntabl.io/blog.


# Limitations
-------------
You cannot use web crawling libraries but you may use a library which scans the html of a 
web page to retrieved url’s embedded within.


# Please consider
-----------------
  * Validation checks and error handling (done)
  * Scalability of running the application on large domains
  * Concurrency
  * Sufficient unit tests
  * Presenting the results

# How to run the app(Dev Mode)
-----------------
  * You can change the url in the app.py and run the app.py to start the program