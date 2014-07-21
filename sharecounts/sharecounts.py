import sys
from datetime import datetime, timedelta
from time import mktime
from redis import Redis
redis = Redis()


urls = ("www.dangayle.com",
        "www.spokesman.com",
        "www.google.com",
        "www.google.com",
        "www.yahoo.com",
        "www.dangayle.com",
        "www.example.com",
        )

def rqueue():
    # for x in xrange(0,10):
    for url in urls:
        print queue_up(url)
    else:
        process_urls()

def queue_up(url):
    """Add url to request queue."""
    return url, redis.zincrby("url_queue",url,1.0)

def push_to_request_queue(url):
    r_queue = redis.hgetall('request_queue')
    timenow = mktime(datetime.now().timetuple())
    print r_queue
    print timenow
    return redis.hset('request_queue',timenow,url)

    # for timestamp in r_queue:
    #     if timestamp < datetime.datetime.now()+timedelta(minute=1)
    #         redis.hdel('request_queue',timestamp)
    # return True
    # if redis.scard("request_queue")

def process_urls():
    """Process url with highest score."""
    processing = redis.zrevrange("url_queue",0,0)
    print "processing %s" % processing[0]
    if push_to_request_queue(processing[0]):
        return redis.zrem("url_queue", processing[0])
    else:
        return None




    # set limit 15 expires 1

def throttle():

    rate = datetime.timedelta(seconds=10)
    print rate.seconds



if __name__ == '__main__':
    rqueue()
    # throttle()
