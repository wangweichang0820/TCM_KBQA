import os
import pickle
import numpy as np


class CLFModel(object):
    def __init__(self, ):
        super(CLFModel, self).__init__()
        self.model_path = 'D:\project\TCM-KBQA\clf\ml_models'
        self.id2label = pickle.load(open(os.path.join(self.model_path, 'id2label.pkl'), 'rb'))
        self.vec = pickle.load(open(os.path.join(self.model_path, 'vec.pkl'), 'rb'))
        self.SVM_clf = pickle.load(open(os.path.join(self.model_path, 'SVM.pkl'), 'rb'))
        self.RFC_clf = pickle.load(open(os.path.join(self.model_path, 'RFC.pkl'), 'rb'))

    def predict(self, text):
        text = ' '.join(list(text.lower()))
        text = self.vec.transform([text])
        proba1 = self.SVM_clf.decision_function(text)
        proba2 = self.RFC_clf.predict_proba(text)
        label = np.argmax((proba1 + proba2) / 2, axis=1)
        return self.id2label.get(label[0])


if __name__ == '__main__':
    model = CLFModel()
    text = '请问感冒了怎么办？'
    label = model.predict(text)
    print(label)
