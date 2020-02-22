import os
import sys
import re
import json
from collections import defaultdict

'''
function to get rid of words and chars that is not necessary and may improve classification

input: file - file path
output: file_content (list) - list of relevant words from file
'''
def tokenize(file):
    stop_words_dict = ['hilton', 'james', 'monaco', 'sofitel', 'affinia', 'ambassador', 'hardrock', 'talbott',
                       'conrad', 'fairmont', 'hyatt', 'omni', 'homewood', 'kickerbocker', 'sheraton', 'swissotel', 'chicaco',
                       'hard', 'rock', 'east', 'allegro', 'amalfi', 'conrad', 'palmer', 'illinois', 'usa', 'midwest',
                        'during', 'has', "its", 'very', 'itself', "whys", 'hers',
                       'isnt', 'off', 'we', 'it', 'the', 'doing', 'over', 'its', 'with',
                       'so', 'but', 'they', 'am', 'until', 'because', "shouldn't", "youre",
                       'is', "theyre", "youd",'themselves', 'or', 'that', 'me', "hows", 'those', 'having',
                       'was', 'and', 'few', 'any', 'being' "mustn't", 'would', 'while', 'should', 'as',
                       "id", "we've", 'when', "wouldnt", 'why', "ill", 'theirs', "aren't",
                       'our', 'from', "wed", 'each', 'only', 'yourself', 'been', 'again',
                       'of', 'a', 'how', 'she', 'you', "were", "theres",
                       'be', 'yours', "heres", 'above', 'at', 'out', 'does'
                        'an', "lets", "theyd",
                       'own', 'his', 'herself', 'before', 'did', 'too', 'here', 'were',
                       "thats",
                       "whats", "shell", 'i', 'all', 'have', "weren't", "you've", "i'm",
                       "hed", 'some', 'into', 'down', 'this', "shed", "ive", 'do',
                       "cant",
                       'for', 'below', 'through', "dont", 'more', 'once', "didn't", 'same',
                       "shes", "theyve", "hell", 'had', 'such', 'cannot', 'about',
                       'myself', 'if', "wont", 'a', 'how', 'she', 'you', "were", "theres",
                       'be', 'yours', "heres", 'above', 'at', 'out', 'does', 'my', 'to',
                       'ought', "hadnt", "doesnt", "couldnt", 'he', 'your', 'ours', 'up',
                       'after', "where's", 'could', 'under', 'nor', 'against', 'further',
                       "theyll",
                       'what', 'then', "youll", 'ourselves', 'which', 'between', "shan't",
                       'these',
                       'in', 'their', "whos", "hes", 'yourselves', 'himself', 'both',
                       "wasnt",
                       'him', 'on', 'them', "whens", 'there', 'where', 'than', 'are', 'her',
                       "hasnt", 'by', 'other', 'who', "haven't", 'most']

    punctuation = '''[.,\/'"#!&\*;$?%\><^:{}=\-_`~()]'''
    file_content = open(file).read()
    file_content = re.sub(punctuation, '', file_content) # get rid of punctuation in file
    file_content = str.split(str.lower(file_content))

    # print('len before ', len(file_content))

    for w in stop_words_dict:
        while w in file_content:
            file_content.remove(w)

    # print('len after ', len(file_content))

    return file_content


if __name__ == '__main__':

    print('Starting main ...')

    input_path = sys.argv[1]

    training_data = defaultdict(list)

    for root, dirs, files in os.walk(input_path):
        if len(dirs) == 0:
            #root.endswith('4') or root.endswith('2') or root.endswith('3'):
            # or root.endswith('1') or root.endswith('2') or root.endswith('3')
            # print(root)
            for file in files:
                if root.rfind('positive') >= 0 and root.rfind('deceptive') >= 0:
                    training_data['positive_deceptive'].append(root + '/' + file)
                elif root.rfind('positive') >= 0 and root.rfind('truthful') >= 0:
                    training_data['positive_truthful'].append(root + '/' + file)
                elif root.rfind('negative') >= 0 and root.rfind('deceptive') >= 0:
                    training_data['negative_deceptive'].append(root + '/' + file)
                elif root.rfind('negative') >= 0 and root.rfind('truthful') >= 0:
                    training_data['negative_truthful'].append(root + '/' + file)

    total_tokens = []
    tokens_by_class = defaultdict(list)
    len_pos = 0
    len_dec = 0
    len_neg = 0
    len_tru = 0

    for class_name, files in training_data.items():
        for file in files:
            file_tokens = tokenize(file)
            for token in file_tokens:
                if token not in total_tokens:
                    total_tokens.append(token)
                if class_name.rfind('positive') >= 0 and class_name.rfind('deceptive') >= 0:
                    tokens_by_class['positive'].append(token)
                    tokens_by_class['deceptive'].append(token)
                    len_pos += 1
                    len_dec += 1
                elif class_name.rfind('positive') >= 0 and class_name.rfind('truthful') >= 0:
                    tokens_by_class['positive'].append(token)
                    tokens_by_class['truthful'].append(token)
                    len_pos += 1
                    len_tru += 1
                elif class_name.rfind('negative') >= 0 and class_name.rfind('deceptive') >= 0:
                    tokens_by_class['negative'].append(token)
                    tokens_by_class['deceptive'].append(token)
                    len_neg += 1
                    len_dec += 1
                elif class_name.rfind('negative') >= 0 and class_name.rfind('truthful') >= 0:
                    tokens_by_class['negative'].append(token)
                    tokens_by_class['truthful'].append(token)
                    len_neg += 1
                    len_tru += 1

    # Calculations that are needed to be done
    #
    # P(c) = total num files in class c / total num files in class c and not c
    # the two classes P(c) should add up to 1 if wanted to check
    # P(word | class c) = (total number of occurrence in the class files + SMOOTHING) / (len(all words in c) +  total words
    # through out class

    cond_prob = defaultdict(list)
    num_total_tokens = len(total_tokens)

    for word in total_tokens:

        if word in tokens_by_class['positive']:
            total_occurrence = tokens_by_class['positive'].count(word)
            denom = float (len(tokens_by_class['positive']) + num_total_tokens) # (len(all words in c) +  total words
            prob = (total_occurrence + 1.5) / denom
            cond_prob[word].append(['positive', prob])

        if word in tokens_by_class['deceptive']:
            total_occurrence = tokens_by_class['deceptive'].count(word)
            denom = float(len(tokens_by_class['deceptive']) + num_total_tokens)
            prob = (total_occurrence + 1.5) / denom
            cond_prob[word].append(['deceptive', prob])

        if word in tokens_by_class['negative']:
            total_occurrence = tokens_by_class['negative'].count(word)
            denom = float(len(tokens_by_class['negative']) + num_total_tokens)
            prob = (total_occurrence + 1.5) / denom
            cond_prob[word].append(['negative', prob])

        if word in tokens_by_class['truthful']:
            total_occurrence = tokens_by_class['truthful'].count(word)
            denom = float(len(tokens_by_class['truthful']) + num_total_tokens)
            prob = (total_occurrence + 1.5) / denom
            cond_prob[word].append(['truthful', prob])

    # P(c) = total num files in class c / total num files in class c and not c
    priors = [['positive', 0.0], ['deceptive', 0.0], ['negative', 0.0], ['truthful', 0.0]]
    priors[0][1] = float(len_pos / (len_pos + len_neg))
    priors[1][1] = float(len_dec / (len_dec + len_tru))
    priors[2][1] = float(len_neg / (len_pos + len_neg))
    priors[3][1] = float(len_tru / (len_tru + len_dec))

    with open('nbmodel.txt', 'w') as nbmodel:
        json.dump(cond_prob, nbmodel)
        nbmodel.write('\n')
        json.dump(priors, nbmodel)

    print('end main ...')