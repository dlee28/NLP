import sys, os, json, re, io
from _collections import defaultdict

stop_words = ['during', 'has', "its", 'very', 'itself', "whys", 'hers',
               'isnt', 'off', 'we', 'it', 'the', 'doing', 'over', 'its', 'with',
               'so', 'but', 'they', 'am', 'until', 'because', "shouldn't", "youre",
               'is', "theyre", "youd",'themselves', 'or', 'that', 'me', "hows", 'those', 'having',
               'was', 'and', 'few', 'any', 'being' "mustn't", 'would', 'while', 'should', 'as',
               "id", "we've", 'when', "wouldnt", 'why', "ill", 'theirs', "aren't",
               'our', 'from', "wed", 'each', 'only', 'yourself', 'been', 'again',
               'of', 'a', 'how', 'she', 'you', "were", "theres",
               'be', 'yours', "heres", 'above', 'at', 'out', 'does', 'an', "lets", "theyd",
               'own', 'his', 'herself', 'before', 'did', 'too', 'here', 'were', "thats",
               "whats", "shell", 'i', 'all', 'have', "weren't", "you've", "i'm",
               "hed", 'some', 'into', 'down', 'this', "shed", "ive", 'do',
               "cant", 'for', 'below', 'through', "dont", 'more', 'once', "didn't", 'same',
               "shes", "theyve", "hell", 'had', 'such', 'cannot', 'about',
               'myself', 'if', "wont", 'a', 'how', 'she', 'you', "were", "theres",
               'be', 'yours', "heres", 'above', 'at', 'out', 'does', 'my', 'to',
               'ought', "hadnt", "doesnt", "couldnt", 'he', 'your', 'ours', 'up',
               'after', "where's", 'could', 'under', 'nor', 'against', 'further',
               "theyll", 'what', 'then', "youll", 'ourselves', 'which', 'between', "shan't",
               'these', 'in', 'their', "whos", "hes", 'yourselves', 'himself', 'both',
               "wasnt", 'him', 'on', 'them', "whens", 'there', 'where', 'than', 'are', 'her',
               "hasnt", 'by', 'other', 'who', "haven't", 'most']

if __name__ == '__main__':
    print('starting main ...')

    model = sys.argv[1]
    path_test_data = sys.argv[2]

    # Key: unique file path Value: defaultdict(Key: words appear in file Value: count)
    testing_data = defaultdict(defaultdict)
    results = defaultdict(str)

    for root, dirs, files in os.walk(path_test_data):
        if len(dirs) == 0:
            for file in files:
                punctuation = '''[.,\/'"#!&\*;$?%\><^:{}=\-_`~()]'''
                with io.open(root + '/' + file, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    file_content = re.sub(punctuation, '', file_content)  # get rid of punctuation in file
                    file_content = str.split(str.lower(file_content))

                for w in stop_words:
                    while w in file_content:
                        file_content.remove(w)

                testing_data[root + '/' + file]

                for word in file_content:
                    if word not in testing_data[root + '/' + file]:
                        testing_data[root + '/' + file][word] = 1
                    else:
                        testing_data[root + '/' + file][word] += 1

    print('finished reading training data ...')

    if model.endswith('vanillamodel.txt'):
        with open(model, 'r', encoding='utf-8') as vanilla:
            lines = vanilla.readlines()
            word_pn = json.loads(lines[0])
            bias_pn = json.loads(lines[1])
            word_td = json.loads(lines[2])
            bias_td = json.loads(lines[3])

        for file_path, count_words in testing_data.items():
            activation_pn = 0.0
            activation_td = 0.0

            for word in count_words.keys():
                if word in word_pn.keys():
                    activation_pn = activation_pn + (word_pn[word] * testing_data[file_path][word])
                if word in word_td.keys():
                    activation_td = activation_td + (word_td[word] * testing_data[file_path][word])

            activation_pn += bias_pn
            activation_td += bias_td
            pos_neg = ''
            tru_dec = ''

            if activation_pn < 0:
                pos_neg = 'negative'
            else:
                pos_neg = 'positive'
            if activation_td < 0:
                tru_dec = 'deceptive'
            else:
                tru_dec = 'truthful'

            results[file_path] = tru_dec + ' ' + pos_neg

        with open('percepoutput.txt', 'w', encoding='utf-8') as percep:
            print('writing file')
            for file_path, classes in results.items():
                percep.write('%s %s \n' % (classes, file_path))

    elif model.endswith('averagedmodel.txt'):
        with open(model, 'r', encoding='utf-8') as avg:
            lines = avg.readlines()
            avg_pn = json.loads(lines[0])
            bias_avg_pn = json.loads(lines[1])
            avg_td = json.loads(lines[2])
            bias_avg_td = json.loads(lines[3])

        for file_path, count_words in testing_data.items():
            activation_pn = 0.0
            activation_td = 0.0

            for word in count_words.keys():
                if word in avg_pn:
                    activation_pn = activation_pn + (avg_pn[word] * testing_data[file_path][word])
                if word in avg_td:
                    activation_td = activation_td + (avg_td[word] * testing_data[file_path][word])

            activation_td += bias_avg_td
            activation_pn += bias_avg_pn
            pos_neg = ''
            tru_dec = ''

            if activation_pn < 0:
                pos_neg = 'negative'
            else:
                pos_neg = 'positive'
            if activation_td < 0:
                tru_dec = 'deceptive'
            else:
                tru_dec = 'truthful'

            results[file_path] = tru_dec + ' ' + pos_neg

        with open('percepoutput.txt', 'w', encoding='utf-8') as percep:
            for file_path, classes in results.items():
                percep.write('%s %s \n' % (classes, file_path))

    print('end main ...')