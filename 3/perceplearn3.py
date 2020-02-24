import sys, os, re, json
from _collections import defaultdict



if __name__ == '__main__':

    print('Starting main ...')

    input_path = sys.argv[1]

    training_data = defaultdict(defaultdict)
    all_words = []

    print('reading training data ...')
    for root, dirs, files in os.walk(input_path):
        if len(dirs) == 0:
            #root.endswith('4') or root.endswith('2') or root.endswith('3'):
            # or root.endswith('1') or root.endswith('2') or root.endswith('3')
            # print(root)

            for file in files:

                punctuation = '''[.,\/'"#!&\*;$?%\><^:{}=\-_`~()]'''
                file_content = open(root + '/' + file).read()
                file_content = re.sub(punctuation, '', file_content)  # get rid of punctuation in file
                file_content = str.split(str.lower(file_content))

                # for w in stop_words_dict:
                #     while w in file_content:
                #         file_content.remove(w)

                training_data[root + '/' + file]

                for word in file_content:
                    if word not in training_data[root + '/' + file]:
                        training_data[root + '/' + file][word] = 1
                    else:
                        training_data[root + '/' + file][word] += 1

                    if word not in all_words:
                        all_words.append(word)
    print('finished reading training data ...')

    bias_pn, bias_td = 0, 0
    bias_avg_pn, bias_avg_td = 0.0, 0.0
    word_pn, word_td = {}, {}
    u_pn, u_td = {}, {}
    avg_pn, avg_td = {}, {}
    beta_pn, beta_td = 0, 0


    for word in all_words:
        word_pn[word] = 0
        word_td[word] = 0
        u_pn[word] = 0
        u_td[word] = 0
        avg_pn[word] = 0
        avg_td[word] = 0

    c = 1
    # perceptron
    for i in range(10):
        for file_path, count_words in training_data.items():
            y_pn, y_td = 0, 0
            a_pn, a_td = 0, 0

            if file_path.rfind('positive') >= 0:
                y_pn = 1
            else:
                y_pn = -1
            if file_path.rfind('truthful') >= 0:
                y_td = 1
            else:
                y_td = -1

            for word in count_words.keys():
                a_pn += training_data[file_path][word] * word_pn[word]
                a_td += training_data[file_path][word] * word_td[word]

            a_pn += bias_pn
            a_td += bias_td

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

    for word in avg_pn.keys():
        avg_pn[word] = float(word_pn[word]) - (float(u_pn[word]) / float(c))
    bias_avg_pn = float(bias_pn) - (float(beta_pn) / float(c))

    for word in avg_td.keys():
        avg_td[word] = float(word_td[word]) - (float(u_td[word]) / float(c))
    bias_avg_td = float(bias_td) - (float(beta_td) / float(c))

    with open('vanillamodel.txt', 'w') as vanilla:
        json.dump(word_pn, vanilla)
        vanilla.write('\n')
        json.dump(bias_pn, vanilla)
        vanilla.write('\n')
        json.dump(word_td, vanilla)
        vanilla.write('\n')
        json.dump(bias_td, vanilla)

    with open('averagedmodel.txt', 'w') as averaged:
        json.dump(avg_pn, averaged)
        averaged.write('\n')
        json.dump(bias_avg_pn, averaged)
        averaged.write('\n')
        json.dump(avg_td, averaged)
        averaged.write('\n')
        json.dump(bias_avg_td, averaged)


    print('end main ...')