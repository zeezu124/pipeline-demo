from flask import Flask, render_template, request, redirect, url_for
from datasets import load_dataset
from joblib import load
import torch as torch
import pandas as pd
import numpy as np
from preprocess import *

pd.set_option('display.max_colwidth', 1000)


class Data:
    def __initII(self, text, labels):
        self.labels = labels
        self.text = text


def get_test_data():
    print("Clicked here")
    test_data_list = []
    count = 10
    
    dataset = load_dataset("go_emotions", "simplified")
    print("loaded data here")
    test = preprocess(dataset=dataset)
    print("preprocess")
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
    print(test[0:1])
    test['prediction'] = pipeline.predict(test['text'][0:1])
    data = str(test['prediction']) + '\n\n'
    print(data)
    #data = str(test.prediction.value_counts()) + '\n\n'
    return data + str(test['text'])


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        result = requestResults()
        return render_template('home.html', result=result)
    return render_template('home.html')


@app.route('/success/<kw>')
def success(kw):
    return "<xmp>" + str(requestResults(kw)) + " </xmp> "


if __name__ == '__main__' :
    app.run(debug=True)