import sys, os, json
from collections import defaultdict

training_words = defaultdict(float) #Key: word from training data Value: count of the word
tag_count = defaultdict(float) #Key: tag from training data Value: count of the tag
transition = defaultdict(float) #Key: previous tag of the current tag Value: count of the previous tag
tag_word = defaultdict(lambda: defaultdict(float)) #Key: tag Value: dict of Key: word Value: count of the pair tag and word
tag_tag = defaultdict(lambda: defaultdict(float)) #Key: previous Value: dic of Key: tag Value: count of the two tags
transition_prob = defaultdict(lambda: defaultdict(float))
emission_prob = defaultdict(lambda: defaultdict(float))


def read_training_data(input_path):
    with open(input_path, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            tag_list = []
            previous = 'START'
            # input file will be structured to have word/tag and a new sentence per new line.
            line_split = line.strip().split()
            for i in range(len(line_split)):
                word = line_split[i].rsplit('/', 1)[0]
                tag = line_split[i].rsplit('/', 1)[1]

                training_words[word] += 1
                tag_count[tag] += 1
                tag_word[tag][word] += 1

                tag_tag[previous][tag] += 1
                transition[previous] += 1

                previous = tag

                if i == len(line_split) - 1:
                    # print(word, tag)
                    tag_tag[previous]['END'] += 1
                    transition[previous] += 1


def check_dic(dic1, dic2):
    count = 0
    print('len dic1: ' , len(dic1.keys()))
    print('len model2: ' , len(dic2.keys()))
    for i in dic2.keys():
        if i not in dic1.keys():
            print('Not in dic1:', i)
    for k, i in dic1.items():
        if dic2[k] != i:
            print('dic1: ' + k, i)
            print('Model2: ' + k, dic2[k])
            count += 1

            # for foo, z in i.items():
            #     if model2[k][foo] == z:
            #         print('Inner Model1: ' + foo, z)
            #         print('Inner Model2: ' + foo, model2[k][foo])
    print('number of difference: ', count)

if __name__ == '__main__':
    print('Starting main ...')

    # path to a single file with training data
    input_path = sys.argv[1]

    # read training data
    read_training_data(input_path)

    # compute emission prob for all tags
    for tag in tag_count.keys():
        for word, count in tag_word[tag].items():
            # count of word/tag divided by total count of tag
            emission_prob[tag][word] = count / tag_count[tag]

    # compute transition prob
    for tag_1 in tag_tag.keys():
        for tag_2 in tag_tag.keys():
            if tag_2 == 'START':
                continue
            transition_prob[tag_1][tag_2] = (tag_tag[tag_1][tag_2] + 1.0) / (transition[tag_1])

    #wrtie to hmmmodel.txt
    with open('hmmmodel.txt', 'w', encoding='utf-8') as f:
        json.dump(training_words, f)
        f.write('\n')
        json.dump(tag_count, f)
        f.write('\n')
        json.dump(emission_prob, f)
        f.write('\n')
        json.dump(transition_prob, f)

    with open('hmmmodel_test.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        training_words_test = json.loads(lines[0])
        transition_prob_test = json.loads(lines[1])
        emission_prob_test = json.loads(lines[2])
        tag_count_test = json.loads(lines[3])

    with open('hmmmodel.txt', 'r', encoding='utf-8') as f1:
        lines = f1.readlines()
        training_words = json.loads(lines[0])
        tag_count = json.loads(lines[1])
        emission_prob = json.loads(lines[2])
        transition_prob = json.loads(lines[3])
