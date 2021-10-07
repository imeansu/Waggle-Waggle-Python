import redis
import json
import time as pytime
from redisqueue import RedisQueue
from bert import Bert
from topicMessage import TopicRequestMessage

class Consumer():

    # consumer 객체 생성
    def __init__(self, name):
        # consumer의 이름
        self.name = name
        self.bert = Bert()
    
    # redis queue consume 연결
    def initConsume(self, q_name, **redis_kwargs):
        # 구독할 큐 연결 
        self.rq = RedisQueue(q_name, **redis_kwargs)

    # while True로 consume 시작
    def startConsume(self):
        # while True: 어떻게 기다리게 하지...?
        msg = self.rq.get(isBlocking=True) # 큐가 비어있을 때 대기
        if msg is not None:
            msg_json = json.loads(msg.decode("utf-8"))
            # bert 추천 로직으로 넘기기
            self.bert.generateTopic(TopicRequestMessage(msg_json["members"], msg_json["sentences"]))
            print(msg_json)




if __name__ == "__main__":
	from redisqueue import RedisQueue
	q = RedisQueue('topic-queue', host='localhost', port=6379, db=0)

	# message get
	import json
	import time as pytime
	while(True):
		msg = q.get(isBlocking=True) 
		if msg is not None:
			msg_json = json.loads(msg.decode('utf-8'))
			print(msg_json)
			pytime.sleep(3) # 결과를 천천히 보기 위해 3 seconds sleep