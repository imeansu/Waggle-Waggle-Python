from topicMessage import *
from topicMessage import TopicResponseMessage
from publisher import Publisher
from BERT_Arch import BERT_Arch2
from BERT_Arch import Run_BERT
from langdetect import detect
from naverClient import naverClient
import requests

class Bert():

    def __init__(self) -> None:
        self.publisher = Publisher("my_queue")
        self.publisher.initPublish("topic", host='redis.slss29.ng.0001.apn2.cache.amazonaws.com', port=6379, db=0)
        self.runBert = Run_BERT()
        self.naverClient = naverClient()
        
#'52.78.117.179'
    def generateTopic(self, topicRequestMessage):
        """
        추천 로직~~~

        """
        sentences = topicRequestMessage.sentences
        for idx, sen in enumerate(sentences):
            if detect(sen) == "ko":
                sentences[idx] = self.papago(sen)
        text = " ".join(topicRequestMessage.sentences)
        result = self.runBert.run(text)
        topicResponseMessage = TopicResponseMessage(topicRequestMessage.members, result)
        self.publisher.publish(topicResponseMessage)
        return 

    def papago(self, text):
        base_url = "https://openapi.naver.com/v1/papago/n2mt"
        headers = {"X-Naver-Client-id": self.naverClient.ClientID, "X-Naver-Client-Secret": self.naverClient.ClientSecret}
        data = {'text' : text, 'source' : 'ko', 'target' : 'en'}
        response = requests.post(base_url, headers=headers, data=data)
        rescode = response.status_code

        if rescode == 200:
            send_data = response.json()
            trans_data = send_data['message']['result']['translatedText']
            print(f"trans_Data : {trans_data}")
            return trans_data
        else:
            print("Error Code: ", rescode)
            return " "


