import pika
import json
import time
from topicMessage import TopicRequestMessage, TopicResponseMessage
from bert import Bert
from functools import partial
from BERT_Arch import BERT_Arch2
from BERT_Arch import Run_BERT

class Consumer:
    def __init__(self):
        self.__url = "13.125.231.62"
        self.__port = 5672
        self.__vhost = "waggle"
        self.__cred = pika.PlainCredentials("guest", "guest")
        self.__queue = "waggle-waggle"
        self.bert = Bert()

    def on_message(channel, method_frame, header_frame, body, self=None):
        body = json.loads(body.decode("utf-8"))
        print(f"Received {body}")
        message = TopicRequestMessage(body["members"], body["sentences"])
        self.bert.generateTopic(message)
        return


    def main(self):
        conn = pika.BlockingConnection(pika.ConnectionParameters(self.__url, self.__port , self.__vhost, self.__cred))
        chan = conn.channel()
        chan.basic_consume(
            queue = self.__queue,
            on_message_callback = partial(Consumer.on_message, self=self),
            auto_ack = True
        )
        print("Consumer is starting...")
        chan.start_consuming()
        return

consumer = Consumer()
consumer.main()