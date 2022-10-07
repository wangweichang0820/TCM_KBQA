import json
import datetime
from py2neo import Graph
from models import OtherQuestion, Triples
from dao import add_other_query, add_triples


class GraphAnswer:
    def __init__(self):
        self.graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))

    def answer_query(self, info_id, query, intent, entity, label):
        '''根据意图和实体构造cql语句'''
        final_answer = ''
        start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if intent == '定义':
            if label == 'SYM':
                add_other_query(OtherQuestion(start_time=start_time, query=query, intent=intent, label=label))
                return '知识不足，无法回答您的问题'
            elif label == 'DES':
                cql = " match (n:疾病)-[r]-(m) where n.name='{0}' return n,m,labels(m),type(r)".format(entity)
                answer = self.graph.run(cql).data()
                if not answer:
                    add_other_query(
                        OtherQuestion(start_time=start_time, query=query, intent=intent, entity=entity, label=label))
                    return '知识不足，无法回答您的问题'
                else:
                    category = set()  # 病类
                    cause = set()  # 病因
                    sym = set()  # 症状
                    for an in answer:
                        add_triples(Triples(info_id, an['n']['name'], '疾病', intent, an['type(r)'], an['m']['name'],
                                            an['labels(m)'][0]))
                        if an['labels(m)'][0] == '病类':
                            category.add(an['m']['name'])
                        elif an['labels(m)'][0] == '病因':
                            cause.add(an['m']['name'])
                        elif an['labels(m)'][0] == '症状':
                            sym.add(an['m']['name'])
                    final_answer = "{0}属于{1}类别，致病的原因主要是{2}，常见的症状有{3}".format(entity, ','.join(list(set(category))),
                                                                             ','.join(list(set(cause))),
                                                                             ','.join(list(set(sym))))

            elif label == 'SYN':
                cql = " match (n:证候)-[r]-(m) where n.name='{0}' return n,m,labels(m),type(r)".format(entity)
                answer = self.graph.run(cql).data()
                # print(answer)
                if not answer:
                    add_other_query(
                        OtherQuestion(start_time=start_time, query=query, intent=intent, entity=entity, label=label))

                    return '知识不足，无法回答您的问题'
                else:
                    treat = set()
                    sym = set()
                    for an in answer:
                        add_triples(Triples(info_id, an['n']['name'], '证候', intent, an['type(r)'], an['m']['name'],
                                            an['labels(m)'][0]))
                        if an['labels(m)'][0] == '治法':
                            treat.add(an['m']['name'])
                        elif an['labels(m)'][0] == '症状':
                            sym.add(an['m']['name'])
                    final_answer = "{0}的常见症状有{2}，可以通过{1}的方法治疗。".format(entity, ','.join(list(set(treat))),
                                                                       ','.join(list(set(sym))))
            elif label == 'PRE':  # 方剂存在重名的情况，因此是多对多的关系,注意空值情况
                cql = " match (n:方剂) where n.proname='{0}' or n.alias='{0}' return n".format(entity)
                answer = self.graph.run(cql).data()
                if not answer:
                    add_other_query(
                        OtherQuestion(start_time=start_time, query=query, intent=intent, entity=entity, label=label))

                    return '知识不足，无法回答您的问题'
                else:
                    temp_answer = ''
                    for an in answer:
                        # print(an)
                        prename = an['n']['proname']
                        temp_answer += "{0}，".format(prename)
                        if an['n']['alias'] != 'nan':
                            add_triples(Triples(info_id, an['n']['proname'], '方剂', '别名', 'alias', an['n']['alias'],
                                                'alias'))

                            temp_answer += "又名{0}，".format(an['n']['alias'])
                        if an['n']['formula'] != 'nan':
                            add_triples(Triples(info_id, an['n']['proname'], '方剂', '配方', 'formula', an['n']['formula'],
                                                'formula'))
                            temp_answer += "配方是：{0}".format(an['n']['formula'])
                        if an['n']['dosage'] != 'nan':
                            add_triples(Triples(info_id, an['n']['proname'], '方剂', '用法用量', 'dosage', an['n']['dosage'],
                                                'dosage'))
                            temp_answer += "用法用量：{0}".format(an['n']['dosage'])
                        if an['n']['classics'] != 'nan':
                            add_triples(
                                Triples(info_id, an['n']['proname'], '方剂', '出自典籍', 'classics', an['n']['classics'],
                                        'classics'))
                            temp_answer += "出自：{0}".format(an['n']['classics'])
                        temp_answer += "\n"
                        # print(temp_answer)
                final_answer = temp_answer
            elif label == 'MED':
                cql = " match (n:药物)-[r]-(m) where n.name='{0}' and (labels(m)=['经络'] or labels(m)=['性味'] or labels(m)=['作用'] or labels(m)=['典籍']) return n,r,m,labels(m),type(r)".format(
                    entity)
                answer = self.graph.run(cql).data()
                # print(answer)
                if not answer:
                    add_other_query(
                        OtherQuestion(start_time=start_time, query=query, intent=intent, entity=entity, label=label))

                    return '知识不足，无法回答您的问题'
                else:
                    xw = set()  # 性味
                    gj = set()  # 归经
                    gx = set()  # 功效
                    dj = set()  # 典籍
                    temp_answer = ''
                    for an in answer:
                        add_triples(Triples(info_id, an['n']['name'], '药物', intent, an['type(r)'], an['m']['name'],
                                            an['labels(m)'][0]))

                        temp_answer += "{0},".format(entity)
                        if an['labels(m)'][0] == '性味':
                            xw.add(an['m']['name'])
                        elif an['labels(m)'][0] == '经络':
                            gj.add(an['m']['name'])
                        elif an['labels(m)'][0] == '作用':
                            gx.add(an['m']['name'])
                        elif an['labels(m)'][0] == '典籍':
                            dj.add(an['m']['name'])
                    final_answer = "{0}具有{1}的性味，归于{2}等经络，具有{3}的功效，记载于{4}。".format(entity, ','.join(list(set(xw))),
                                                                                  ','.join(list(set(gj))),
                                                                                  ','.join(list(set(gx))),
                                                                                  ','.join(list(set(dj))))


        elif intent == '病因':
            if label == 'DES':
                cql = "match (n:疾病)-[r:病因]-(m) where n.name='{0}' return n,r,m,labels(m),type(r)".format(entity)
                answer = self.graph.run(cql).data()
                if not answer:
                    add_other_query(
                        OtherQuestion(start_time=start_time, query=query, intent=intent, entity=entity, label=label))

                    return '知识不足，无法回答您的问题'
                else:
                    cause = set()
                    for an in answer:
                        cause.add(an['m']['name'])
                        add_triples(Triples(info_id, an['n']['name'], '疾病', intent, an['type(r)'], an['m']['name'],
                                            an['labels(m)'][0]))
                    final_answer = "{0}的病因是{1}。".format(entity, ','.join(list(set(cause))))
            else:
                add_other_query(OtherQuestion(start_time=start_time, query=query, intent=intent, label=label))

                return '知识不足，无法回答您的问题'
        elif intent == '症状':
            if label == 'DES' or label == 'SYN':
                cql = "match (n)-[r:症状]-(m) where n.name='{0}' return n,r,m,labels(m),type(r)".format(entity)
                answer = self.graph.run(cql).data()
                if not answer:
                    add_other_query(
                        OtherQuestion(start_time=start_time, query=query, intent=intent, entity=entity, label=label))

                    return '知识不足，无法回答您的问题'
                else:
                    sym = set()
                    for an in answer:
                        node_type = ''
                        if label == "DES":
                            node_type = '疾病'
                        else:
                            node_type = '证候'
                        add_triples(Triples(info_id, an['n']['name'], node_type, intent, an['type(r)'], an['m']['name'],
                                            an['labels(m)'][0]))
                        sym.add(an['m']['name'])
                    final_answer = "{0}的症状主要有：{1}。".format(entity, ','.join(list(set(sym))))
            else:
                return '知识不足，无法回答您的问题'
        elif intent == '症状疾病':
            if label == 'SYM':
                cql = "match (n:症状)-[r:症状]-(m) where n.name contains '{0}' return n,m,labels(m),type(r)".format(entity)
                answer = self.graph.run(cql).data()
                if not answer:
                    return '知识不足，无法回答您的问题'
                else:
                    syn = set()
                    des = set()
                    for an in answer:
                        # print(an)
                        add_triples(Triples(info_id, an['n']['name'], '症状', intent, an['type(r)'], an['m']['name'],
                                            an['labels(m)'][0]))
                        if an['labels(m)'][0] == '疾病':
                            des.add(an['m']['name'])
                        elif an['labels(m)'][0] == '证候':
                            syn.add(an['m']['name'])
                    final_answer = "{0}可能由{1}{2}等病、证导致。".format(entity, ','.join(list(set(des))),
                                                                ','.join(list(set(syn))))
            else:
                add_other_query(OtherQuestion(start_time=start_time, query=query, intent=intent, label=label))

                return '知识不足，无法回答您的问题'
        elif intent == '治法':
            if label == 'DES' or label == 'SYM':
                cql = "MATCH (n)-[r:`主治`]-(m) where m.name='{0}' return n,m,labels(n),type(r)".format(entity)
                answer = self.graph.run(cql).data()
                # print(answer)
                if not answer:
                    add_other_query(
                        OtherQuestion(start_time=start_time, query=query, intent=intent, entity=entity, label=label))

                    return '知识不足，无法回答您的问题'
                else:
                    pre = set()
                    med = set()
                    temp_answer = '能够治疗{0}的'.format(entity)
                    for an in answer:
                        add_triples(Triples(info_id, an['n']['name'], an['labels(n)'][0], intent, an['type(r)'],
                                            an['m']['name'], label))
                        if an['labels(n)'][0] == '方剂':
                            pre.add(an['n']['proname'])
                        elif an['labels(n)'][0] == '药物':
                            med.add(an['n']['name'])
                    if len(pre) > 0 & len(med) > 0:
                        temp_answer += "方剂有{0}等，药物有{1}等。".format(','.join(list(set(pre))), ','.join(list(set(med))))
                    elif len(pre) > 0 & len(med) == 0:
                        temp_answer += "有{0}等方剂。".format(','.join(list(set(pre))))
                    else:
                        temp_answer += "有{0}等药物。".format(','.join(list(set(med))))
                    final_answer = temp_answer
            elif label == 'SYN':
                cql = "match (n)-[r:`治法证候`]-(m) where n.name='{0}' return n,m,labels(m),type(r)".format(entity)
                answer = self.graph.run(cql).data()
                if not answer:
                    add_other_query(
                        OtherQuestion(start_time=start_time, query=query, intent=intent, entity=entity, label=label))

                    return '知识不足，无法回答您的问题'
                else:
                    tre = set()
                    for an in answer:
                        add_triples(Triples(info_id, an['n']['name'], '证候', intent, an['type(r)'],
                                            an['m']['name'], an['labels(m)'][0]))
                        tre.add(an['m']['name'])
                    final_answer = "{0}常见治疗方法有：{1}。".format(entity, ','.join(list(set(tre))))
            else:
                add_other_query(
                    OtherQuestion(start_time=start_time, query=query, intent=intent, label=label))

                return '知识不足，无法回答您的问题'
        elif intent == '主治':
            if label == 'PRE':
                cql = "match (n:方剂)-[r:主治]-(m) where n.proname='{0}' or n.alias='{0}' return n,m,labels(m),type(r)".format(
                    entity)
                answer = self.graph.run(cql).data()
                # print(answer)
                if not answer:
                    add_other_query(
                        OtherQuestion(start_time=start_time, query=query, intent=intent, entity=entity, label=label))

                    return '知识不足，无法回答您的问题'
                else:
                    pre_name = set()  # 集合
                    answers = []  # 列表
                    for an in answer:
                        add_triples(Triples(info_id, an['n']['name'], '方剂', intent, an['type(r)'],
                                            an['m']['name'], an['labels(m)'][0]))
                        temp_answer = {}  # 字典
                        # print(an['n']['name'], an['m']['name'])
                        pre_name.add(an['n']['name'])

                        name = an['n']['name']
                        pro_name = an['n']['proname']
                        alias = an['n']['alias']
                        classics = an['n']['classics']
                        symptom = an['m']['name']
                        temp_answer['name'] = name
                        temp_answer['proname'] = pro_name
                        temp_answer['alias'] = alias
                        temp_answer['classics'] = classics
                        temp_answer['symptom'] = symptom
                        answers.append(temp_answer)

                    temp_answers = []
                    temp = []
                    # print(tail)
                    # print(trail)

                    for i in pre_name:
                        sym = set()
                        for an in answers:
                            # print(an)
                            if i == an.get('name'):
                                temp = an
                                sym.add(an.get('symptom'))
                            else:
                                continue
                            temp['symptom'] = ','.join(list(set(sym)))
                        temp_answers.append(temp)

                    temp = set()
                    for an in temp_answers:
                        answer_temp = "{0},".format(an.get('proname'))
                        if an.get('alias') != 'nan':
                            answer_temp += "又名{0}".format(an.get('alias'))
                        if an.get('symptom') != 'nan':
                            answer_temp += "能够主治的病症有：{0}".format(an.get('symptom'))
                        if an.get('classics') != 'nan':
                            answer_temp += "，出自{0}".format(an.get('classics'))
                        temp.add(answer_temp)
                    final_answer = '\n'.join(list(set(temp)))

            elif label == 'MED':
                cql = "match (n:药物)-[r:主治]-(m) where n.name = '{0}'  return n,m,labels(m),type(r)".format(entity)
                answer = self.graph.run(cql).data()
                if not answer:
                    return '知识不足，无法回答您的问题'
                else:
                    sym = set()
                    for an in answer:
                        add_triples(Triples(info_id, an['n']['name'], '药物', intent, an['type(r)'],
                                            an['m']['name'], an['labels(m)'][0]))
                        sym.add(an['m']['name'])
                final_answer = "{0}能够主治的病症主要有：{1}。".format(entity, ','.join(list(set(sym))))
        else:
            add_other_query(
                OtherQuestion(start_time=start_time, query=query, intent=intent, label=label))

            return '知识不足，无法回答您的问题'

        return final_answer


if __name__ == '__main__':
    g = GraphAnswer()
    res = g.answer_query(2, '', '主治', '白芷', 'MED')
    print(res)
