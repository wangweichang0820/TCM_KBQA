from functools import reduce
from flask import Flask, render_template, request, json
from question_pro import AnswerSearch
from dao import *

app = Flask(__name__)
app.config.from_object(__name__)
# 禁用严格的斜线以支持您的需求
app.url_map.strict_slashes = False


@app.route('/', strict_slashes=False)
def QA_mian():
    qa_list = query_qa_list()
    return render_template('index.html', qa_list=qa_list)


# 回复详情页面
@app.route('/replydetail/<id>', methods=['GET', 'POST'], strict_slashes=False)
def replydetail(id):
    qa_detail = query_qa_id(id)
    triples = query_triples_id(id)

    node_labels = set()

    tri = []
    head_node = []
    tail_node = []
    link = []
    categories = []

    for t in triples:
        result = {}
        head = {}
        tail = {}
        edge = {}
        node_labels.add(t.tail_label)
        node_labels.add(t.head_label)
        result['head'] = str(t.head)
        result['head_label'] = str(t.head_label)
        result['relation'] = str(t.relation)
        result['relation_type'] = str(t.relation_type)
        result['tail'] = str(t.tail)
        result['tail_label'] = str(t.tail_label)

        head['name'] = str(t.head)
        head['des'] = ''
        head['symbolSize'] = 60
        head['category'] = str(t.head_label)

        tail['name'] = str(t.tail)
        tail['des'] = ''
        tail['symbolSize'] = 50
        tail['category'] = str(t.tail_label)

        edge['source'] = str(t.head)
        edge['target'] = str(t.tail)
        edge['name'] = str(t.relation)
        edge['des'] = str(t.tail_label)

        tri.append(result)
        head_node.append(head)
        tail_node.append(tail)
        link.append(edge)

    head_node = remove_list_dict_duplicate(head_node)
    tail_node = remove_list_dict_duplicate(tail_node)

    for i in node_labels:
        temp = {}
        temp['name'] = i
        categories.append(temp)

    node = json.dumps((head_node + tail_node), ensure_ascii=False)
    categories = json.dumps(categories, ensure_ascii=False)
    link = json.dumps(link, ensure_ascii=False)

    node_label_len = len(node_labels)

    return render_template('ReplyDetail.html', qa_detail=qa_detail, node=node, link=link, categories=categories,
                           node_label_len=node_label_len)


# 常见问题页面
@app.route('/FQA', methods=['GET', 'POST'], strict_slashes=False)
def FQA():
    DES_num = query_qa_re_counte('DES')
    SYN_num = query_qa_re_counte('SYN')
    SYM_num = query_qa_re_counte('SYM')
    MED_num = query_qa_re_counte('MED')
    PRE_num = query_qa_re_counte('PRE')
    total_num = query_qa_re_counte()
    qa_list = query_qa_all()
    return render_template('FQA.html', DES_num=DES_num, SYN_num=SYN_num, SYM_num=SYM_num, MED_num=MED_num,
                           PRE_num=PRE_num, total_num=total_num, qa_list=qa_list)


# 关键字检索结果页面
@app.route('/qasearch/', methods=['GET', 'POST'], strict_slashes=False)
def qasearch():
    keyword = request.form.get('keyword')
    print(keyword)
    qa_list = query_qa_keyword(keyword)
    return render_template('QaList.html', keyword=keyword, qa_list=qa_list)


# label检索结果页面
@app.route('/qa_label_list/<label>', methods=['GET', 'POST'], strict_slashes=False)
def qa_label_list(label):
    qa_list = query_qa_label(label)
    return render_template('QaList.html', qa_list=qa_list)


# 全部检索结果页面
@app.route('/qalist/', methods=['GET', 'POST'], strict_slashes=False)
def qalist():
    qa_list = query_qa_list()
    return render_template('QaList.html', qa_list=qa_list)


# 答案检索
@app.route('/answer_search/', methods=['POST'], strict_slashes=False)
def answer_search():
    query = request.form.get('text')
    answersearch = AnswerSearch()
    answer = answersearch.question_clf(query)
    # print(answer)
    return json.dumps({'answer': answer})


# 对list格式的dict进行去重
def remove_list_dict_duplicate(list_dict_data):
    run_function = lambda x, y: x if y in x else x + [y]
    return reduce(run_function, [[], ] + list_dict_data)


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000)
