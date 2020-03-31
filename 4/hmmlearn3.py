import sys, os
from collections import defaultdict

training_words = defaultdict(float) #Key: word from training data Value: count of the word
tag_count = defaultdict(float) #Key: tag from training data Value: count of the tag
transition = defaultdict(float) #Key: previous tag of the current tag Value: count of the previous tag
tag_word = defaultdict(lambda: defaultdict(float)) #Key: tag and word Value: count of the pair tag and word
tag_tag = defaultdict(lambda: defaultdict(float)) #Key: previous tag to current tag Value: count of the two tags
transition_prob = defaultdict(lambda: defaultdict(float))
emission_prob = defaultdict(lambda: defaultdict(float))


def read_training_data(input_path):
    with open(input_path, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            tag_list = []
            previous = 'start'
            # input file will be structured to have word/tag and a new sentence per new line.
            for word_tag in line.strip().split():
                word = word_tag.rsplit('/', 1)[0]
                tag = word_tag.rsplit('/', 1)[1]

                training_words[word] += 1
                tag_count[tag] += 1
                tag_word[tag][word] += 1

                tag_tag[previous][tag]_+= 1
                transition[previous] += 1

                previous = tag
                # print(word, tag)


    print(tag_list)

if __name__ == '__main__':
    print('Starting main ...')


    # path to a single file with training data
    input_path = sys.argv[1]

    # read training data
    read_training_data(input_path)

    # transition_probabilities = defaultdict(lambda: defaultdict(float))
    # print(transition_probabilities[0])