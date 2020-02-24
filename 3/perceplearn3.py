import sys, os, re
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

    bias_pn  = 0
    word_pn = {}
    u_pn = {}
    avg_pn = {}
    beta_pn = 0

    bias_td = 0
    word_td = {}
    u_td = {}
    avg_td= {}
    beta_td = 0
    c = 1


    print('end main ...')