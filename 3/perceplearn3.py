import sys, os, re, json, io
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

    print('Starting main ...')

    input_path = sys.argv[1]

    # Key: unique file path Value: defaultdict(Key: words appear in file Value: count)
    training_data = defaultdict(defaultdict)
    all_words = []

    print('reading training data ...')
    for root, dirs, files in os.walk(input_path):
        if len(dirs) == 0:
            for file in files:

                punctuation = '''[.,\/'"#!&\*;$?%\><^:{}=\-_`~()]'''
                with io.open(root + '/' + file, 'r', encoding='utf8') as f:
                    file_content = f.read()
                    file_content = re.sub(punctuation, '', file_content)  # get rid of punctuation in file
                    file_content = str.split(str.lower(file_content))

                for w in stop_words:
                    while w in file_content:
                        file_content.remove(w)

                training_data[root + '/' + file]

                for word in file_content:

                    if word not in training_data[root + '/' + file]:
                        training_data[root + '/' + file][word] = 1
                    else:
                        training_data[root + '/' + file][word] += 1

                    if word not in all_words:
                        all_words.append(word)
    print('finished reading training data ...')

    # initialize bias
    bias_pn, bias_td = 0, 0
    bias_avg_pn, bias_avg_td = 0.0, 0.0
    word_pn, word_td = {}, {}
    u_pn, u_td = {}, {}
    avg_pn, avg_td = {}, {}
    beta_pn, beta_td = 0.0, 0.0

    # initialize weights
    for word in all_words:
        word_pn[word] = 0
        word_td[word] = 0
        u_pn[word] = 0
        u_td[word] = 0
        avg_pn[word] = 0
        avg_td[word] = 0

    c = 1 # counter for avg model
    # perceptron
    print('perceptron started ...')
    for i in range(10):
        for file_path, count_words in training_data.items():
            y_pn, y_td = 0, 0 # reset y and a for every file
            a_pn, a_td = 0, 0

            # for our training dataset, we know the class names are in the file path
            if file_path.rfind('positive') >= 0:
                y_pn = 1
            else:
                y_pn = -1
            if file_path.rfind('truthful') >= 0:
                y_td = 1
            else:
                y_td = -1

            # compute activation
            for word in count_words.keys():
                a_pn += training_data[file_path][word] * word_pn[word]
                a_td += training_data[file_path][word] * word_td[word]

            a_pn += bias_pn
            a_td += bias_td

            # only update weights and bias if ya is less equal to 0
            if a_pn * y_pn <= 0:
                for word in training_data[file_path].keys():
                    word_pn[word] = word_pn[word] + (y_pn * training_data[file_path][word])
                    u_pn[word] = u_pn[word] + (y_pn * c * training_data[file_path][word])
                bias_pn += y_pn
                beta_pn = beta_pn + (y_pn * c)

            if a_td * y_td <= 0:
                for word in training_data[file_path].keys():
                    word_td[word] = word_td[word] + (y_td * training_data[file_path][word])
                    u_td[word] = u_td[word] + (y_td * c * training_data[file_path][word])
                bias_pn += y_td
                beta_td = beta_td + (y_td * c)

            c += 1

    # make calculations for averaged model
    # w - (u / c), b - (beta / c)
    for word in avg_pn.keys():
        avg_pn[word] = float(word_pn[word]) - (float(u_pn[word]) / float(c))
    bias_avg_pn = float(bias_pn) - (float(beta_pn) / float(c))

    for word in avg_td.keys():
        avg_td[word] = float(word_td[word]) - (float(u_td[word]) / float(c))
    bias_avg_td = float(bias_td) - (float(beta_td) / float(c))

    print('perceptron ended ... ')
    print('writing to files vanillamodel.txt , averagedmodel.txt ...')

    # write in the order of
    # word_pn, bais_pn, word_td, bias_td
    # make sure to read in the same order when classifying
    with open('vanillamodel.txt', 'w', encoding='utf-8') as vanilla:
        json.dump(word_pn, vanilla)
        vanilla.write('\n')
        json.dump(bias_pn, vanilla)
        vanilla.write('\n')
        json.dump(word_td, vanilla)
        vanilla.write('\n')
        json.dump(bias_td, vanilla)

    # write in the order of
    # avg_pn, bais_avg_pn, avg_td, bias_avg_td
    # make sure to read in the same order when classifying
    with open('averagedmodel.txt', 'w', encoding='utf-8') as averaged:
        json.dump(avg_pn, averaged)
        averaged.write('\n')
        json.dump(bias_avg_pn, averaged)
        averaged.write('\n')
        json.dump(avg_td, averaged)
        averaged.write('\n')
        json.dump(bias_avg_td, averaged)

    print('done writing files ...')
    print('end main ...')