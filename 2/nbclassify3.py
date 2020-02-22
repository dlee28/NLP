import json
import os
import sys
import math
from collections import defaultdict
from nblearn3 import tokenize

if __name__ == '__main__':
    print('starting main ...')

    input_path = sys.argv[1]

    testing_data = defaultdict(list)
    output = defaultdict(list)

    with open('nbmodel.txt', 'r') as nbmodel:
        lines = nbmodel.readlines()
        cond_prob = json.loads(lines[0]) # {'word', [['class', p], ... ]
        priors = json.loads(lines[1]) # [['positive', float] ... ]

    for root, dirs, files in os.walk(input_path):
        if len(dirs) == 0:
            # root.endswith('1')
            for file in files:
                testing_data[root].append(root+'/'+file)

    output = defaultdict(list)

    for root, test_files in testing_data.items():
        for file in test_files:
            pos_prob = 0.0
            des_prob = 0.0
            neg_prob = 0.0
            tru_prob = 0.0
            file_tokens = tokenize(file)
            for word in file_tokens:
                class_prob = cond_prob.get(word)

                if class_prob is not None and len(class_prob) == 4:
                    pos_prob += math.log(class_prob[0][1])  # pos
                    des_prob += math.log(class_prob[1][1])  # des
                    neg_prob += math.log(class_prob[2][1])  # neg
                    tru_prob += math.log(class_prob[3][1])  # tru
                # print(pos_prob, des_prob, neg_prob, tru_prob)

            # add priors
            pos_prob += priors[0][1]
            des_prob += priors[1][1]
            neg_prob += priors[2][1]
            tru_prob += priors[3][1]

            classes = ''

            if des_prob > tru_prob:
                classes += 'deceptive '
                # output[file].append('deceptive')
            else:
                # output[file].append('truthful')
                classes += 'truthful '
            if pos_prob > neg_prob:
                # output[file].append('positive')
                classes += 'positive'
            else:
                # output[file].append('negative')
                classes += 'negative'

            output[file].append(classes)

            # print(classes)

    with open('nboutput.txt', 'w') as nboutput:
        for key, classes in output.items():
            nboutput.write('%s %s\n' % (classes[0], key))

    print('ending main ... ')