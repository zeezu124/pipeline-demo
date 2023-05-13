from flask import Flask, render_template, request
from datasets import load_dataset
from joblib import load
import torch as torch
import pandas as pd
from preprocess import preprocess

pd.set_option('display.max_colwidth', 1000)


class Data:
    def __initII(self, text, labels):
        self.labels = labels
        self.text = text


def get_test_data():
    print("Clicked here")
    test_data_list = []
    
    dataset = load_dataset("go_emotions", "simplified")
    print("loaded data here")
    test = preprocess(dataset=dataset)
    print("preprocess")
    
    #reduced test df to about 26 rows to reduce runtime
    test = test[~test.index.isin(range(0, 5400))]
    print('Row Count of test:', len(test))
    arr1 = []
    arr2= []
    for data in test['text']:
        arr1.append(data)
    for data in test['labels']:
        arr2.append(data.item())


    for v1, v2 in zip(arr1, arr2):
        test_data_list.append((v1, v2))
    '''test_data_list.append({
        'text' : data.text,
        'labels': data.labels,
    })'''
    return pd.DataFrame(test_data_list, columns= ["text", "labels"])

pipeline = load("twitter_roberta_cpu_2.joblib")
#pipeline = torch.load(pipeline, map_location=torch.device('cpu'))



def requestResults():
    
    test = get_test_data()
    test['prediction'] = pipeline.predict(test['text'].to_list())
    #data = str(test['prediction']) + '\n\n'
    data = str(test.prediction.value_counts()) + '\n\n'
    return data + str(test['text'])


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        return "<xmp>" + str(requestResults()) + "</xmp>"
    return render_template('home.html')
    
    
if __name__ == '__main__' :
    app.run(debug=True)