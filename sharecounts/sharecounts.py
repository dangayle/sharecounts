from __future__ import print_function
import sys
from datetime import datetime, timedelta
from time import time, sleep
from redis import Redis
import requests
redis = Redis()


URLS = (
        "www.spokesman.com",
        "www.google.com",
        "www.yahoo.com",
        "www.example.com",
        "www.gibberish.com",
        "www.a.com",
        "www.b.com",
        "www.c.com",
        "www.d.com",
        "www.forza.com",
        "www.bbc.co.uk",
        "www.canada.ca",
        "www.twitter.com",
        "www.amazon.com"
        )


def sharecount(url):
    """Get social share count for given url."""
    queue_url(url)
    process_urls()
    print(url, get_share_count(url))


def queue_url(url):
    """Add url to request queue and/or increase score."""
    return url, redis.zincrby("url_queue",url,1.0)


def push_to_requested_queue(url):
    """Flush request queue and """

    time_period = timedelta(seconds=30).seconds
    requests_per_period = 15  # Twitter API

    print("Processing: {}".format(url))
    timenow = time()
    requested_queue = redis.hgetall('requested_queue')

    for rurl, timestamp in requested_queue.items():
        time_diff = timenow - float(timestamp)
        if time_diff > time_period:
            # Flush old requests
            redis.hdel('requested_queue',rurl)
            requested_queue.pop(rurl, None)

    count = redis.hlen('requested_queue')

    if not url in requested_queue and count < requests_per_period:
        redis.hset('requested_queue',url,timenow)
        twitter(url)
        return True


def twitter(url):
    r = requests.get('http://urls.api.twitter.com/1/urls/count.json?url={}&callback=?'.format(url))
    if r.status_code == 200:
        count = r.json().get('count',0)
        redis.hset(url,"twitter_count",count)
        return count


def process_urls():
    """Process url with highest score."""

    processing = redis.zrevrange("url_queue",0,0)
    if push_to_requested_queue(processing[0]):
        return redis.zrem("url_queue", processing[0])


def get_share_count(url):
    return redis.hgetall(url)


if __name__ == '__main__':

    for url in URLS:
        sharecount(url)
        sleep(10)
