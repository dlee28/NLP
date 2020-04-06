import sys, os, json
from collections import defaultdict

training_words = defaultdict(float)
tag_count = defaultdict(float)
emission_prob = defaultdict(lambda: defaultdict(float))
transition_prob = defaultdict(lambda: defaultdict(float))
decoded = []

def viterbi(words_line):
    tag = []
    prob = []
    backpointer = []
    tags = list(tag_count.keys())
    curr_emission = 0.0
    max_prob = -100.0


    for i in range(len(tags)):
        prob.append([0.0] * len(words_line))
        backpointer.append([0.0] * len(words_line))

    for i in range(len(tags)):
        #calculation for if the start is known from our training words
        f_word = words_line[0]
        curr_tag = tags[i]

        if f_word in training_words.keys():
            if curr_tag not in emission_prob.keys():
                curr_emission = 0.0
            else:
                if emission_prob[curr_tag].get(f_word) is not None:
                    curr_emission = emission_prob[curr_tag][f_word]
                else:
                    curr_emission = 0.0
            prob[i][0] = transition_prob['START'][curr_tag] * curr_emission
        else:
            # print('tag: ', tag)
            prob[i][0] = transition_prob['START'][curr_tag]

        backpointer[i][0] = 0.0

    for i in range(1, len(words_line)):
        for j in range(len(tags)):
            curr_prob = 0.0
            max_prob = -100.0
            index_max_prob = -1
            for p in range(len(tags)):
                if words_line[i] in training_words.keys():
                    if tags[j] not in emission_prob.keys():
                        curr_emission = 0.0
                    else:
                        if emission_prob[tags[j]].get(words_line[i]) is not None:
                            curr_emission = emission_prob[tags[j]][words_line[i]]
                        else:
                            curr_emission = 0.0
                    curr_prob = transition_prob[tags[p]][tags[j]] * prob[p][i - 1] * curr_emission

                else:
                    curr_prob = transition_prob[tags[p]][tags[j]] * prob[p][i - 1]

                if max_prob < curr_prob:
                    max_prob = curr_prob
                    index_max_prob = p

            prob[j][i] = max_prob
            backpointer[j][i] = index_max_prob




if __name__ == '__main__':
    print('Starting main ...')

    input_path = sys.argv[1]

    with open('hmmmodel.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        training_words = json.loads(lines[0])
        tag_count = json.loads(lines[1])
        emission_prob = json.loads(lines[2])
        transition_prob = json.loads(lines[3])

    print('starting viterbi ...')

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            words_line = line.strip().split()
            viterbi(words_line)


    output_file = 'hmmscore.txt'


