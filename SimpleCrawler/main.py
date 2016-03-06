import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'sebastianwalter'
HOMEPAGE = 'http://sebastianwalter.org'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 2
thread_queue = Queue()
# very first spider, creates list and folder and gets all urls from the staring page
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)


# Create worker threads (will die when main exists); _ means I do not care about the value it self
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = thread_queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        thread_queue.task_done()


# Each queue link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        thread_queue.put(link)
    thread_queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0 :
        print(str(len(queued_links))+ ' links in the queue')
        create_jobs()



create_workers()
crawl()