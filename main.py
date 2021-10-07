# from redisqueue import ReidsQueue
from consumer import Consumer
# q = RedisQueue('topic-queue', host='localhost', port=6379, db=0)

consumer = Consumer("my_queue")
consumer.initConsume('topic-queue', host='localhost', port=6379, db=0)
while True:
    consumer.startConsume()
    
