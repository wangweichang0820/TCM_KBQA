# -*- coding:utf-8 -*-

import os
import time
import pickle
import random
import numpy as np
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
# KNN分类算法
from sklearn.neighbors import KNeighborsClassifier
from sklearn import naive_bayes
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

seed = 222
random.seed(seed)
np.random.seed(seed)


def load_data(data_path):
    X, y = [], []
    with open(data_path, 'r', encoding='utf8') as f:
        for line in f.readlines():
            text, label = line.strip().split('\t')
            text = ' '.join(list(text.lower()))
            X.append(text)
            y.append(label)

    index = np.arange(len(X))
    np.random.shuffle(index)
    X = [X[i] for i in index]
    y = [y[i] for i in index]
    return X, y


def run(data_path, model_save_path):
    X, y = load_data(data_path)

    label_set = sorted(list(set(y)))
    label2id = {label: idx for idx, label in enumerate(label_set)}
    id2label = {idx: label for label, idx in label2id.items()}

    y = [label2id[i] for i in y]

    label_names = sorted(label2id.items(), key=lambda kv: kv[1], reverse=False)
    target_names = [i[0] for i in label_names]
    labels = [i[1] for i in label_names]

    train_X, text_X, train_y, text_y = train_test_split(X, y, test_size=0.2, random_state=42)

    vec = TfidfVectorizer(ngram_range=(1, 3), min_df=0, max_df=0.9, analyzer='char', use_idf=1, smooth_idf=1,
                          sublinear_tf=1)
    train_X = vec.fit_transform(train_X)
    text_X = vec.transform(text_X)

    since = time.time()

    # -------------SVM--------------
    # SVM = svm.LinearSVC(tol=0.00001, C=5.0, multi_class='crammer_singer',class_weight='balanced',random_state=122, max_iter=1500)
    # SVM.fit(train_X, train_y)
    # pred = SVM.predict(text_X)
    # print("SVM模型结果")
    # print(classification_report(text_y, pred, target_names=target_names))
    # print(confusion_matrix(text_y, pred, labels=labels))

    # -------------LR--------------
    # LR = LogisticRegression(C=5, dual=False, n_jobs=4, max_iter=400, multi_class='auto', random_state=122)
    # LR.fit(train_X, train_y)
    # pred = LR.predict(text_X)
    # print("LR模型结果")
    # print(classification_report(text_y, pred,target_names=target_names))
    # print(confusion_matrix(text_y, pred,labels=labels))

    # -------------gbdt--------------
    # gbdt = GradientBoostingClassifier(n_estimators=450, learning_rate=0.001,max_depth=8, random_state=24)
    # gbdt.fit(train_X, train_y)
    # pred = gbdt.predict(text_X)
    # print("gbdt模型结果")
    # print(classification_report(text_y, pred,target_names=target_names))
    # print(confusion_matrix(text_y, pred,labels=labels))

    # -------------决策树--------------
    # DTC = tree.DecisionTreeClassifier(criterion='entropy', random_state=122, splitter='random')
    # DTC.fit(train_X, train_y)
    # pred = DTC.predict(text_X)
    # print("决策树模型结果")

    # -------------随机森林--------------
    # RFC = RandomForestClassifier()
    # RFC.fit(train_X, train_y)
    # pred = RFC.predict(text_X)
    # print("随机森林模型结果")

    # 构建knn分类模型，并指定 k 值
    KNN = KNeighborsClassifier(n_neighbors=10)
    KNN.fit(train_X, train_y)
    pred = KNN.predict(text_X)
    print("KNN模型结果")

    # 构建朴素贝叶斯分类模型（未实现）
    # GNB = naive_bayes.GaussianNB()  # 高斯贝叶斯
    # GNB.fit(train_X, train_y)
    # pred = GNB.predict(text_X)
    # print("GNB模型结果")

    time_elapsed = time.time() - since
    print('Training complete in {:.0f}m {:.4f}s'.format(time_elapsed // 60, time_elapsed % 60))
    print(classification_report(text_y, pred, digits=4, target_names=target_names))
    print(confusion_matrix(text_y, pred, labels=labels))
    # -------------融合--------------
    # pred_prob1 = LR.predict_proba(text_X)
    # pred_prob2 = gbdt.predict_proba(text_X)
    #
    # pred = np.argmax((pred_prob1+pred_prob2)/2, axis=1)
    # print('融合结果')
    # print(classification_report(text_y, pred,target_names=target_names))
    # print(confusion_matrix(text_y, pred,labels=labels))
    #
    # pickle.dump(id2label,open(os.path.join(model_save_path,'id2label.pkl'),'wb'))
    # pickle.dump(vec,open(os.path.join(model_save_path,'vec.pkl'),'wb'))
    # # pickle.dump(LR,open(os.path.join(model_save_path,'LR.pkl'),'wb'))
    # # pickle.dump(gbdt,open(os.path.join(model_save_path,'gbdt.pkl'),'wb'))
    # pickle.dump(SVM, open(os.path.join(model_save_path, 'SVM.pkl'), 'wb'))
    # pickle.dump(RFC, open(os.path.join(model_save_path, 'RFC.pkl'), 'wb'))


if __name__ == '__main__':
    run("./datasets/TCM/合并.txt", "model_file")
