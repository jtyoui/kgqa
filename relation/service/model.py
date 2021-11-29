import torch
import torch.nn as nn
from pytorch_pretrained_bert import BertModel, BertTokenizer

key = {0: '别名',
       1: '分布区域',
       2: '病原学名',
       3: '病原中文名',
       4: '病原属性',
       5: '为害部位',
       6: '为害作物',
       7: '属目',
       8: '属科',
       9: '学名',
       10: '防治药物',
       11: '症状',
       12: '病原',
       13: '传播途径和发病条件',
       14: '病因',
       15: '防治方法',
       16: '为害特点',
       17: '形态特征',
       18: '生活习性',
       19: '生态特点',
       20: '生态史',
       21: '简介'
       }


class Config:
    """配置参数"""

    def __init__(self):
        self.dir = '/app/model/'
        self.class_list = [str(i) for i in range(len(key))]  # 类别名单
        self.save_path = self.dir + 'ERNIE'
        self.device = torch.device('cpu')
        self.require_improvement = 1000  # 若超过1000batch效果还没提升，则提前结束训练
        self.num_classes = len(self.class_list)  # 类别数
        self.num_epochs = 3  # epoch数
        self.batch_size = 128  # mini-batch大小
        self.pad_size = 32  # 每句话处理成的长度(短填长切)
        self.learning_rate = 5e-5  # 学习率
        self.bert_path = self.dir + 'bert'
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)
        self.hidden_size = 768

    def build_dataset(self, text):
        lin = text.strip()
        pad_size = len(lin)
        token = self.tokenizer.tokenize(lin)
        token = ['[CLS]'] + token
        token_ids = self.tokenizer.convert_tokens_to_ids(token)
        mask = [1] * pad_size
        token_ids = token_ids[:pad_size]
        return torch.tensor([token_ids], dtype=torch.long), torch.tensor([mask])


class Model(nn.Module):

    def __init__(self, config):
        super(Model, self).__init__()
        self.bert = BertModel.from_pretrained(config.bert_path)
        for param in self.bert.parameters():
            param.requires_grad = True
        self.fc = nn.Linear(config.hidden_size, config.num_classes)

    def forward(self, x):
        context = x[0]
        mask = x[1]
        _, pooled = self.bert(context, attention_mask=mask, output_all_encoded_layers=False)
        out = self.fc(pooled)
        return out


config = Config()
model = Model(config).to(config.device)
model.load_state_dict(torch.load(config.save_path, map_location='cpu'))


def prediction_model(text):
    """输入一句问话预测"""
    data = config.build_dataset(text)
    with torch.no_grad():
        outputs = model(data)
        num = torch.argmax(outputs)
    return key[int(num)]


if __name__ == '__main__':
    print(prediction_model('大麻跳甲的学名？？'))
