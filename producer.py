import redis
import json
import time as pytime
from redisqueue import RedisQueue
from topicMessage import TopicRequestMessage

class Producer():

    # producerer 객체 생성
    def __init__(self, name):
        # consumer의 이름
        self.name = name

    # redis queue produce 연결
    def initProduce(self, q_name,**redis_kwargs):
        # 발행할 큐 연결 
        self.rq = RedisQueue(q_name, **redis_kwargs)

    def produce(self, topicResponseMessage):
        cur_time = '{"timestamp":' + str(pytime.time()) + '}'
        message_str = json.dumps(topicResponseMessage)
        print(message_str)
        self.rq.put(message_str)


if __name__ == "__main__":
	from redisqueue import RedisQueue
	q = RedisQueue('my-queue', host='localhost', port=6379, db=0)

	# message put
	import json
	import time as pytime
	for i in range(30):
		cur_time = '{"timestamp":' + str(pytime.time()) + '}'
		element  = json.loads(cur_time)

		# Add Your Own Data
		element['id']   = i

		element_str = json.dumps(element)
		print(element_str)
		q.put(element_str)