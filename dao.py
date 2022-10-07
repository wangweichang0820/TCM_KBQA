from sqlalchemy.orm import sessionmaker

from models import get_engine, QaInfo, Triples


def get_session():
    engine = get_engine()
    db_session = sessionmaker(bind=engine)
    return db_session()


def add_info(qa):
    session = get_session()
    session.add(qa)
    session.commit()
    print("add info succeed")
    session.close()


def add_triples(triples):
    session = get_session()
    session.add(triples)
    session.commit()
    print("add triples succeed")
    session.close()


def add_other_query(oq):
    session = get_session()
    session.add(oq)
    session.commit()
    print("add oq succeed")
    session.close()


def query_qa_all():
    session = get_session()
    qa_info = session.query(QaInfo).filter(QaInfo.adopt > 0).all()
    session.close()
    return qa_info


def query_qa_one(entity=None, relation=None):
    session = get_session()
    qa_info = session.query(QaInfo).filter(QaInfo.head == entity, QaInfo.relation == relation,
                                           QaInfo.adopt > 0).order_by(QaInfo.start_time.desc()).first()
    session.close()
    if qa_info:
        return qa_info.answer
    else:
        return ''


def query_qa_maxid():
    session = get_session()
    maxid = session.query(QaInfo).order_by(QaInfo.ID.desc()).first()
    session.close()
    return maxid.ID


def query_qa_id(id):
    session = get_session()
    qa_info = session.query(QaInfo).filter_by(ID=id).first()
    session.close()
    return qa_info


def query_triples_id(id):
    session = get_session()
    triples = session.query(Triples).filter(Triples.info_id == id).all()
    session.close()
    return triples


def query_qa_label(label):
    session = get_session()
    qa_info = session.query(QaInfo).filter(QaInfo.label == label).order_by(QaInfo.start_time.desc()).all()
    session.close()
    return qa_info


def query_qa_keyword(keyword):
    session = get_session()
    qa_info = session.query(QaInfo).filter(QaInfo.query.like('%{0}%'.format(keyword))).all()
    session.close()
    return qa_info


def query_qa_list():
    session = get_session()
    qa_info = session.query(QaInfo).filter(QaInfo.adopt > 0).limit(6).all()
    session.close()
    return qa_info


def query_qa_re_counte(label=None):
    session = get_session()
    if label != None:
        count = session.query(QaInfo).filter(QaInfo.label == label, QaInfo.adopt > 0).count()
    else:
        count = session.query(QaInfo).filter(QaInfo.adopt > 0).count()
    session.close()
    return count


def print_all(infos):
    answer = [info.answer for info in infos]
    return answer


def update_user(id):
    session = get_session()
    session.query(QaInfo).filter(QaInfo.ID == id).update({"adopt": 1})
    session.commit()
    session.close()


def delete_user(id):
    session = get_session()
    session.query(QaInfo).filter(QaInfo.id == id).delete()
    session.commit()
    session.close()


if __name__ == '__main__':
    # init_db()

    # add_user(lisi)
    # answer = query_qa_one()
    # print(answer)

    # new = QaInfo('2022-05-14', '小柴胡汤能够治疗感冒吗？', '小柴胡汤', 'PRE', '主治', '可以', 0)
    # add_info(new)
    # triples = Triples(2, '', '', '', '', '', '')
    # add_triples(triples)

    # fqa_list = query_qa_list()
    # for fqa in fqa_list:
    #     print("{0},{1},{2}".format(fqa.id, fqa.head, fqa.label))

    # qa_detail = query_qa_re_counte('主治')
    # for qa in qa_detail:
    #     print(qa.id, qa.query)

    # qa_list = query_qa_label('MED')
    # for qa in qa_list:
    #     print(qa.id, qa.query)

    # qa_list = query_qa_keyword('蜂蜜')
    # for qa in qa_list:
    #     print(qa.id, qa.query)

    # maxid = query_qa_maxid()
    # print(maxid)

    # triples = query_triples_id(36)
    # result = {}
    # head = set()
    # s = []
    #
    # for t in triples:
    #     result = {}
    #     result['head'] = str(t.head)
    #     result['head_label'] = str(t.head_label)
    #     head.add(result['head'])
    #     s.append(result)
    #
    # s = json.dumps(s, ensure_ascii=False)
    # hr = json.dumps(list(head), ensure_ascii=False)
    #
    # print(triples)
    # print(result)
    # print(s)
    # print(head)
    # print(hr)

    count = query_qa_re_counte()
    print(count)
