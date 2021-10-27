from topicMessage import *
from topicMessage import TopicResponseMessage
from publisher import Publisher

class Bert():

    def __init__(self) -> None:
        self.publisher = Publisher("my_queue")
        self.publisher.initPublish("topic", host='52.78.117.179', port=6379, db=0)

    def generateTopic(self, topicMessage):
        """
        추천 로직~~~

        """
        topicResponseMessage = TopicResponseMessage(topicMessage.members, list(["k-pop", "김치", "twice"]))
        self.publisher.publish(topicResponseMessage)
        return 