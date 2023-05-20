from tqdm import tqdm

def fourteen_labels(x, multi = False): # cuts down to 14 unique labels
    
    if multi is False:
        x = x[0]
    if x == 2 or x == 10 or x == 11:
        return 3
    elif x == 15 or x == 18 or x == 4 or x == 21:
        return 0
    elif x == 16 or x == 9 or x == 24 or x == 12:
        return 25
    elif x == 13 or x == 17:
        return 1
    elif x == 19:
        return 14
    else:
        return x
    
def new_labels(x, multi = False): # updates labels to be between 0-13
    
    if multi is False:
        x = x[0]
    if x == 0:
        return 0
    elif x == 1:
        return 1
    elif x == 3:
        return 2
    elif x == 5:
        return 3
    elif x == 6:
        return 4
    elif x == 7:
        return 5
    elif x == 8:
        return 6
    elif x == 14:
        return 7
    elif x == 20:
        return 8
    elif x == 22:
        return 9
    elif x == 23:
        return 10
    elif x == 25:
        return 11
    elif x == 26:
        return 12
    elif x == 27:
        return 13
    

def replace_labels(labels):
  for i in tqdm(range(len(labels))):
    if len(labels[i]) == 1:
        labels[i] = [fourteen_labels(labels[i])]
        labels[i] = [new_labels(labels[i])]
        
    else:
        for j in range(len(labels[i])):
            labels[i][j] = fourteen_labels(labels[i][j], multi = True)
            labels[i][j] = new_labels(labels[i][j], multi = True)
    
  return labels

def class_freq(data):
    class_freq = {} #create a dic of class freq. for visualisation purposes
    classes = list(range(0,14))
    for x in classes:
        class_freq[x] = 0
    for x in data['labels']:
        if len(x) == 1:
            class_freq[x[0]] +=1
    else:
        for j in x:
            class_freq[j] +=1
    return class_freq

def remove_dupes(data): #stops a data point from having same class label more than once
    z = []
    for x in data:
        z.append(list(dict.fromkeys(x)))
    return z


def multilabel2multiclass(ls, class_dict):
    class_dict = class_dict
    for i in range(len(ls)):
        if len(ls[i]) > 1:
            temp = []
            for j in range(len(ls[i])):
                temp.append(ls[i][j])
                temp2 = {}
                for x in temp:
                    temp2[x] = class_dict[x]
            ls[i] = [min(temp2)]
    return ls

def num2word(x): # converts numbers back to class names for visualisation purposes
    if x == 0:
        return 'admiration'
    if x == 1:
        return 'amusement'
    if x == 2:
        return 'annoyance'
    if x == 3:
        return 'caring'
    if x == 4:
        return 'confusion'
    if x == 5:
        return 'curiosity'
    if x == 6:
        return 'desire'
    if x == 7:
        return 'fear'
    if x == 8:
        return 'optimism'
    if x == 9:
        return 'realisation'
    if x == 10:
        return 'relief'
    if x == 11:
        return 'sadness'
    if x == 12:
        return 'surprise'
    if x == 13:
        return 'neutral'

def format(x, text):
    label = x[0]['label'][6:]
    label = num2word(int(label))
    string = f"The text: {text} | denotes this emotion: {label} | with a confidence score of {str(x[0]['score'])}"
    return string

def format_output(predictions, input_text):
    formatted_output = []
    for prediction in predictions:
        label = prediction['label'][6:]
        label = num2word(int(label))
        score = prediction.get('score', None)  # Get the confidence score or None if not present
        
        output_dict = {
            'text': input_text,
            'emotion': label,
            'score': score
        }
        
        formatted_output.append(output_dict)
    
    return formatted_output


def format_output2(predictions, input_text):
    formatted_output = []
    for prediction in predictions:
        label = prediction['label'][6:]
        label = num2word(int(label))
        score = prediction.get('score', None)  # Get the confidence score or None if not present
        if score is not None:
            string = f"The text: {input_text} | denotes this emotion: {label} | with a confidence score of {str(score)}"
        else:
            string = f"The text: {input_text} | denotes this emotion: {label}"
        formatted_output.append(string)
    return formatted_output


def format_output1(predictions, input_text):
    formatted_output = []
    for prediction in predictions:
        label = prediction['label'][6:]
        label = num2word(int(label))
        string = f"The text: {input_text} | denotes this emotion: {label} | with a confidence score of {str(prediction['score'])}"
        formatted_output.append(string)
    return formatted_output


def requestResults():
    
    test = get_test_data()
    test = test['text'].to_list()
    testtext = test[24]
    ans = pipeline.predict(testtext)

    #data = str(test['prediction']) + '\n\n'
    #data = str(test.prediction.value_counts()) + '\n\n'
    return format(ans, testtext)

