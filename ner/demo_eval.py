import time
import torch
from transformers import BertTokenizer, AlbertTokenizer
from ner.bert_for_ner import BertCrfForNer
from ner.albert_for_ner import AlBertCrfForNer


class NER_predict():
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else 'cpu'
        self.label2idx = {"O": 0, "B-PRE": 1, "I-PRE": 2, "B-MED": 3, "I-MED": 4, "B-DES": 5, "I-DES": 6, "B-SYM": 7,
                          "I-SYM": 8, "B-SYN": 9, "I-SYN": 10}
        self.idx2label = {idx: label for label, idx in self.label2idx.items()}

        '''bert 应用配置'''
        # self.path_model = 'bert'  # 测试路径
        self.path_model = 'D:\\project\\TCM-KBQA\\ner\\bert'  # 系统应用路径
        self.tokenizer = BertTokenizer.from_pretrained(self.path_model)
        self.model = BertCrfForNer.from_pretrained(self.path_model)
        '''Albert应用配置'''
        # self.path_model = 'D:\\project\\TCM-KBQA\\ner\\albert'
        # self.path_model = 'albert'
        # self.tokenizer = BertTokenizer.from_pretrained(self.path_model)
        # self.model = AlBertCrfForNer.from_pretrained(self.path_model)

        self.model.to(self.device)
        self.model.eval()

    def predict_ner(self, text):
        inputs = self.tokenizer(
            text,
            max_length=256,
            truncation="longest_first",
            return_tensors="pt")
        inputs = inputs.to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs[0]
            batch_predict_labels = self.model.crf.decode(logits, inputs['attention_mask'])

        predict_labels = batch_predict_labels[0][1:-1]  # [CLS]XXXX[SEP] 每次只有一条数据
        print(predict_labels)
        pred_labels = [self.idx2label[ix] for ix in predict_labels]
        chars = self.tokenizer.convert_ids_to_tokens(inputs.input_ids[0][1:-1])
        pred_entities = self.extract(chars, pred_labels)
        return pred_entities

    # 输出结果
    def extract(self, chars, tags):
        result = []
        pre = ''
        w = []
        for idx, tag in enumerate(tags):
            if not pre:
                if tag.startswith('B'):
                    pre = tag.split('-')[1]
                    w.append(chars[idx])
            else:
                if tag == f'I-{pre}':
                    w.append(chars[idx])
                else:
                    result.append([w, pre])
                    w = []
                    pre = ''
                    if tag.startswith('B'):
                        pre = tag.split('-')[1]
                        w.append(chars[idx])
        res = [[''.join(x[0]), x[1]] for x in result]
        # print(res)
        return res


if __name__ == '__main__':
    sentence = '小柴胡汤可以治疗感冒吗？'
    since = time.time()
    predictor = NER_predict()

    res = predictor.predict_ner(sentence)
    for ner_res in res:
        entity = ner_res[0]
        label = ner_res[1]
        print(entity, label)
    time_end = time.time() - since

    print(f'Predicted NER: {res}')
    print('所需时间：{:.0f}M{:.4f}s'.format(time_end // 60, time_end % 60))

    print('---------------\n')
