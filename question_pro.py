import datetime

from clf.clf_model import CLFModel
from cls.Predictor import Predictor
from ner.demo_eval import NER_predict
from graphsearch import GraphAnswer
from models import *
from dao import *


class AnswerSearch:

    def question_clf(self, query):
        clfmodel = CLFModel()
        first_intent = clfmodel.predict(query)
        print(first_intent)

        if (first_intent != 'diagnosis'):
            return '你好，我可以回答中医相关问题。'
        else:
            '''实体关系抽取'''
            re_predict = Predictor()
            intent = re_predict.predict(query)
            print(intent)
            start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if intent == '其他':
                add_other_query(OtherQuestion(start_time=start_time, query=query, intent='其他'))
                return '知识不足，回答不了您的问题。'
            else:
                '''命名实体识别'''
                ner_predict = NER_predict()
                ner_res = ner_predict.predict_ner(query)
                if len(ner_res) > 0:
                    answer = ''
                    for ner in ner_res:
                        entity = ner[0]
                        label = ner[1]
                        temp_answer = query_qa_one(entity, intent)
                        if temp_answer:
                            answer += temp_answer + '\n'
                        else:
                            print('FQA数据库中无此记录')
                            info_id = query_qa_maxid() + 1
                            g = GraphAnswer()
                            ganswer = g.answer_query(info_id, query, intent, entity, label)
                            answer += ganswer
                            # 将问答记录存储在数据库
                            qa_info = QaInfo(start_time, query, entity, label, intent, answer, 1)
                            add_info(qa_info)
                    return answer
                else:
                    add_other_query(
                        OtherQuestion(start_time=start_time, query=query, intent=intent))
                    return '知识不足，回答不了您的问题。'


if __name__ == '__main__':
    answersearch = AnswerSearch()
    text = '小柴胡汤可以治疗感冒吗？'
    answer = answersearch.question_clf(text)
    print(answer)
