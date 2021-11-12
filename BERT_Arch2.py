import torch
import json
from torch import nn
from pytorch_pretrained_bert import BertModel
from pytorch_pretrained_bert import BertTokenizer
from keras.preprocessing.sequence import pad_sequences

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
        x = self.softmax(x)VB
        return x
    
class Run_BERT:
    def __init__(self):
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
        piped = self.text_pipeline(text)
        text = torch.tensor(piped).to(self.device)
        masks = torch.tensor(self.text_masks(piped)).to(self.device)
        output = self.model(text, masks)
        return output.cpu().detach().numpy()[0]
    
    def run(self, text, num_result=5):
        result = self.predict(text)
        return [self.num_to_label[str(i)] for i in result.argsort()[::-1][:num_result]]