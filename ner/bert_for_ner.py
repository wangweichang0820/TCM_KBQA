# -*- coding: utf-8 -*
import torch
import torch.nn as nn
from ner.crf import CRF
from transformers import BertPreTrainedModel, BertModel


class BertCrfForNer(BertPreTrainedModel):
    def __init__(self, config):
        super(BertCrfForNer, self).__init__(config)
        self.BaseModel = BertModel(config)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.classifier = nn.Linear(config.hidden_size, config.num_labels)
        self.crf = CRF(num_tags=config.num_labels, batch_first=True)
        self.init_weights()

    def forward(self, input_ids, token_type_ids=None, attention_mask=None, labels=None, input_lens=None):
        outputs = self.BaseModel(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        sequence_output = outputs[0]
        sequence_output = self.dropout(sequence_output)
        logits = self.classifier(sequence_output)
        outputs = (logits,)
        if labels is not None:
            labels = torch.where(labels >= 0, labels, torch.zeros_like(labels))        
            loss = self.crf(emissions = logits, tags=labels, mask=attention_mask)
            outputs = (-1*loss,) + outputs
        return outputs  # (loss), scores
