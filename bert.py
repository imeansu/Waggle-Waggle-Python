from topicMessage import *
from topicMessage import TopicResponseMessage
from publisher import Publisher
from BERT_Arch import BERT_Arch2
from BERT_Arch import Run_BERT

class Bert():

    def __init__(self) -> None:
        self.publisher = Publisher("my_queue")
        self.publisher.initPublish("topic", host='redis.slss29.ng.0001.apn2.cache.amazonaws.com', port=6379, db=0)
        self.runBert = Run_BERT()
        
#'52.78.117.179'
    def generateTopic(self, topicRequestMessage):
        """
        추천 로직~~~

        """
        text = " ".join(topicRequestMessage.sentences)
        result = self.runBert.run(text)
        topicResponseMessage = TopicResponseMessage(topicRequestMessage.members, result)
        self.publisher.publish(topicResponseMessage)
        return 
