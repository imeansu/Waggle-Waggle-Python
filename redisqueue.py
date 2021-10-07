import redis
class RedisQueue(object):
    """
        Redis Lists are an ordered list, First In First Out Queue
        Redis List pushing new elements on the head (on the left) of the list.
        The max length of a list is 4,294,967,295
    """
    def __init__(self, name, **redis_kwargs):
        """
            host='localhost', port=6379, db=0
        """
        self.key = name
        self.rq = redis.Redis(**redis_kwargs)

    def size(self): # 큐 크기 확인
        return self.rq.llen(self.key)

    def isEmpty(self): # 비어있는 큐인지 확인
        return self.size() == 0

    def put(self, element): # 데이터 넣기
        self.rq.rpush(self.key, element) # right push

    def get(self, isBlocking=False, timeout=None): # 데이터 꺼내기
        if isBlocking:
            element = self.rq.blpop(self.key, timeout=timeout) # blocking left pop
            element = element[1] # key[0], value[1]
        else:
            element = self.rq.lpop(self.key) # left pop
        return element

    def get_without_pop(self): # 꺼낼 데이터 조회
        if self.isEmpty():
            return None
        element = self.rq.lindex(self.key, -1)
        return element