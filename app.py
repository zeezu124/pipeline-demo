from flask import Flask, render_template, request, jsonify
from datasets import load_dataset
from joblib import load
import torch as torch
import pandas as pd
from preprocess import preprocess
from utils import format
import datetime

pd.set_option('display.max_colwidth', 1000)

log_file_path = 'log.txt'

class Data:
    def __initII(self, text, labels):
        self.labels = labels
        self.text = text


def log_interaction(input_text, prediction):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current timestamp
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'Timestamp: {timestamp}\n')
        log_file.write(f'Input: {input_text}\n')
        log_file.write(f'Prediction: {prediction}\n')
        log_file.write('\n')  # Add a new line for separation


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
    text = test['text']
    test['prediction'] = pipeline.predict(test['text'].to_list())
    #data = str(test['prediction']) + '\n\n'
    data = test.prediction
    answers = []
    for i in range(0, len(data)):
        answers.append(format([data[i]], text[i]))
    
    #print(data)
    #return list(data) + list(test['text']) #+ str(test['text'])
    return answers


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST', 'GET'])
def get_data1():
    if request.method == 'POST':
        return "<xmp>\n" + "\n".join(requestResults()) + "</xmp>"
    return render_template('home.html')

@app.route('/predict', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
            
            input_text = request.form['input_text']  # Get the input text from the form
            prediction = pipeline.predict([input_text])  # Make prediction on the input text using the pipeline
            string = format(prediction, input_text)
            log_interaction(input_text, string)
            return render_template('result.html', prediction=string)  # Display the prediction in the result.html template
            #return(jsonify(string))
    
    return render_template('home.html')
    

@app.route('/results', methods=['POST'])
def predict():
    if 'input_text' in request.json:
        input_text = request.json['input_text']  # Get the input text from the request
        prediction = pipeline.predict([input_text])  # Make prediction on the input text using the pipeline
        #predicted_label = prediction# Assuming prediction is a single label
        #changed from format to format_output
        string = format_output(prediction, input_text)
        log_interaction(input_text, string)
        return jsonify({'output': string})  # Return predicted label as JSON response
    
    return jsonify({'error': 'Invalid request'})

@app.route('/results_json', methods=['POST'])
def predict1():
    if 'input_text' in request.json:
        input_text = request.json['input_text']  # Get the input text from the request
        prediction = pipeline.predict([input_text])  # Make prediction on the input text using the pipeline
        #predicted_label = prediction# Assuming prediction is a single label
        #changed from format to format_output
        string = format_output(prediction, input_text)
        log_interaction(input_text, string)
        return jsonify({'output': string})  # Return predicted label as JSON response
    
    return jsonify({'error': 'Invalid request'})


    
    
if __name__ == '__main__' :
    app.run(debug=True)