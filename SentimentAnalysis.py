from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoModel, TFAutoModel
from transformers import RobertaTokenizer
from transformers import TFRobertaForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
import pandas as pd
from scipy.special import softmax
import csv
import urllib.request

task='sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
tokenizer = AutoTokenizer.from_pretrained(MODEL)

def convert_example_to_feature(review):
    return roberta_tokenizer.encode_plus(review,
                                         add_special_tokens=True,
                                         max_length=max_length,
                                         pad_to_max_length=True,
                                         return_attention_mask=True,
                                         )
def encode_examples(ds, limit=-1):
    input_ids_list = []
    attention_mask_list = []
    label_list = []
    
    if (limit > 0):
        ds = ds.take(limit)
    
    for review, label in tfds.as_numpy(ds):
        bert_input = convert_example_to_feature(review.decode())
        input_ids_list.append(bert_input['input_ids'])
        attention_mask_list.append(bert_input['attention_mask'])
        label_list.append([label])
    
    return tf.data.Dataset.from_tensor_slices((input_ids_list,
                                               attention_mask_list,
                                               label_list)).map(map_example_to_dict)



# download label mapping
labels=[]
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')
labels = [row[1] for row in csvreader if len(row) > 1]

model = TFAutoModelForSequenceClassification.from_pretrained(MODEL)

score_list = []
text_list = []
i=0
with open('/Users/macintosh/Desktop/CSV Text Only Files/NYU_All.csv',encoding = "ISO-8859-1") as read_obj:
    csv_reader = csv.reader(read_obj)
    for row in csv_reader:
        for text in row:
            encoded_input = tokenizer(text, return_tensors='tf')
            output = model(encoded_input)
            scores = output[0][0].numpy()
            scores = softmax(scores)
            score_list.append(scores)
            text_list.append(text)
        i=i+1
        print(i," Sentences Encoded")

label_list = []
appended = False
for scores,text in zip(score_list,text_list):
    print(text)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    appended = False
    for i in range(scores.shape[0]):
        l = labels[ranking[i]]
        if not appended:
            appended = True
            label_list.append(l)
        s = scores[ranking[i]]
        print(f"{i+1}) {l} {np.round(float(s), 4)}")
    print("\n")
score_list = pd.DataFrame(score_list, columns=['neg','neu','pos'])
score_list['Label'] = label_list
score_list.to_csv(r'/Users/macintosh/Desktop/NYU_SA_All.csv',index = False, header=True)

