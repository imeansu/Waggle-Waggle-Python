import torch
import json
from torch import nn
from pytorch_pretrained_bert import BertModel
from pytorch_pretrained_bert import BertTokenizer
from keras.preprocessing.sequence import pad_sequences
from pytrends.request import TrendReq
import pandas as pd
import time

class BERT_Arch2(nn.Module):
    def __init__(self, dropout=0.1):
        super(BERT_Arch2, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.linear = nn.Linear(768,41)
        self.softmax = nn.LogSoftmax(dim=1)

    #define the forward pass
    def forward(self, sent_id, mask=None):
        #pass the inputs to the model  
        _, cls_hs = self.bert(sent_id, attention_mask=mask)
        x = self.linear(cls_hs)
        x = self.softmax(x)
        return x

class Run_BERT:
    def __init__(self):
        self.tmp = ['bts', 'blackpink', 'netflix', 'korean_food', 'nct', 'kpop', 'squid_game', 'twice', 'north_korea', 'itzy']
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
        self.device = torch.device("cpu")
        self.model = torch.load('./model_v1.pt', map_location=self.device)

        with open("num_to_label.json", 'r') as json_file:
            self.num_to_label = json.load(json_file)

    def text_pipeline(self, text):
        tmp = tuple(['[CLS]'] + self.tokenizer.tokenize(text)[:510] + ['[SEP]'])
        return pad_sequences(list(map(self.tokenizer.convert_tokens_to_ids,[tmp])), maxlen=512, truncating="post", padding="post", dtype="int")

    def text_masks(self, texts):
        return [[float(i > 0) for i in ii] for ii in texts]

    def predict(self, text):
        origin_text = text
        piped = self.text_pipeline(text)
        text = torch.tensor(piped).to(self.device)
        masks = torch.tensor(self.text_masks(piped)).to(self.device)
        output = self.model(text, masks)
        output = output.cpu().detach().numpy()[0]
        for i in self.num_to_label:
            word = self.num_to_label[i]
            if word in origin_text.lower() and word in self.tmp:
                output[int(i)] += 5
            if word not in self.tmp:
                output[int(i)] -= 100
        output[7] -= 3
        return output
    
    def google_trend(self, topic):
        topic = topic.replace("_", " ")
        print(f"topic is : {topic}")
        kw_list = [topic]
        pytrends = TrendReq(hl="ko", tz=540)
        pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='KR', gprop='')
        related_topics = pytrends.related_topics()
        # print(related_topics)
        # print("-------------")
        df = pytrends.related_queries()
        df = pd.DataFrame(df[topic]["rising"])
        related_queries = df["query"].values
        return related_queries

    def run(self, text, num_result=5):
        start = time.time()
        result = self.predict(text)
        result = [self.num_to_label[str(i)] for i in result.argsort()[::-1][:num_result]]
        print(f"BERT_Arch result: {result}")
        result = result[:2]
        try: 
            query = "넷플릭스" if result[0] == "netflix" else result[0]
            google_trends = list(self.google_trend(query))
            print(f"google_trend : {google_trends}")
            result.extend(google_trends[:1])
        except Exception as e: 
            print("Exception message: ", e)
            pass
        print(f"BERT + google: {result}")
        print(f"take time : {time.time() - start}")
        return result