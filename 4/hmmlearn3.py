import sys, os
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


if __name__ == '__main__':
    print('Starting main ...')

    # path to a single file with training data
    input_path = sys.argv[1]

    # read training data
    read_training_data(input_path)

    # compute emmission prob for all tags
    for tag in tag_count.keys():
        for word, count in tag_word[tag].items():
            # count of word/tag divided by total count of tag
            emission_prob[tag][word] = count / tag_count[tag]

    # compute transition prob
    # for tag in tag_tag.keys():
    #     for after_tag in tag_tag.keys():




