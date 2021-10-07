import redis
import json
import time as pytime
from redisqueue import RedisQueue
from topicMessage import TopicRequestMessage

class Publisher():

    # publisher 객체 생성
    def __init__(self, name):
        # consumer의 이름
        self.name = name

    # redis publisher 연결
    def initPublish(self, channel_name, **redis_kwargs):
        # 발행할 큐 연결 
        self.channel_name = channel_name
        self.rq = redis.Redis(**redis_kwargs)

    def publish(self, topicResponseMessage):
        cur_time = '{"timestamp":' + str(pytime.time()) + '}'
        message_str = json.dumps({"members":topicResponseMessage.members, "topics": topicResponseMessage.topics})
        print(message_str)
        return self.rq.publish(self.channel_name, message_str)


if __name__ == "__main__":
	pass