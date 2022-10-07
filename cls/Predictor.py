import os
import time

import torch
import torch.nn as nn
from transformers import BertTokenizer, BertPreTrainedModel, BertModel, AlbertPreTrainedModel, AlbertModel,AlbertTokenizer


class Bert(BertPreTrainedModel):

    def __init__(self, config):
        super(Bert, self).__init__(config)
        self.bert = BertModel(config)
        self.hidden_size = config.hidden_size
        self.num_classes = config.num_labels
        self.fc = nn.Linear(self.hidden_size, self.num_classes)

    def forward(self,
                input_ids,
                token_type_ids,
                attention_mask,
                label=None,
                input_ids_anti=None,
                label_anti=None):
        # inference
        output_bert = self.bert(input_ids, attention_mask=attention_mask)  # (batch_size, sen_length, hidden_size)
        output_pooler = output_bert.pooler_output
        output = self.fc(output_pooler)

        return [output, output_pooler]


class Albert(AlbertPreTrainedModel):

    def __init__(self, config):
        super(Albert, self).__init__(config)
        self.albert = AlbertModel(config)
        self.hidden_size = config.hidden_size
        self.num_classes = config.num_labels
        self.fc = nn.Linear(self.hidden_size, self.num_classes)

    def forward(self, input_ids, attention_mask, label=None):
        output = self.albert(input_ids, attention_mask=attention_mask)
        output_pooler = output.pooler_output
        output = self.fc(output_pooler)
        return [output, output_pooler]


class Predictor():

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else 'cpu'
        self.label = [x.strip() for x in open('cls/class.txt', 'r', encoding='utf8').readlines()]
        # self.label = [x.strip() for x in open('cls\class.txt', 'r', encoding='utf8').readlines()]
        self.label2ids = {x: i for i, x in enumerate(self.label)}
        self.ids2label = {i: x for i, x in enumerate(self.label)}

        # 加载模型
        # path_model = 'bert'
        path_model = 'cls/bert'
        path_config = 'cls/bert/config.json'
        # path_config = 'bert/config.json'
        self.tokenizer = BertTokenizer.from_pretrained(path_model)
        self.model = Bert.from_pretrained(path_model, config=path_config)
        # self.model = Albert.from_pretrained(path_model, config=path_config)

    def predict(self, text):
        """
        预测
        """
        # print('predict start')
        self.model.to(self.device)
        self.model.eval()

        inputs = self.tokenizer(
            text,
            max_length=256,
            truncation="longest_first",
            return_tensors="pt")
        inputs = inputs.to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            label = torch.max(outputs[0].data, 1)[1].tolist()
            res = self.label[label[0]]
            # print(res)
            return res


if __name__ == '__main__':
    text = '请问感冒了怎么办？'
    since = time.time()
    predictor = Predictor()
    res = predictor.predict(text)
    time_end = time.time() - since
    print("分类结果:" + res)
    print('所需时间：{:.0f}M{:.4f}s'.format(time_end // 60, time_end % 60))
