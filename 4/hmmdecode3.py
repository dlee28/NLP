import sys, os, json
from collections import defaultdict

# https://web.stanford.edu/~jurafsky/slp3/8.pdf
# http://www.cs.jhu.edu/~jason/465/hw-hmm/hw-hmm.pdf
# https://nlp.stanford.edu/~wcmac/papers/20050421-smoothing-tutorial.pdf

training_words = defaultdict(float) #Key: word from training data Value: count of the word
tag_count = defaultdict(float) #Key: tag from training data Value: count of the tag
emission_prob = defaultdict(lambda: defaultdict(float))
transition_prob = defaultdict(lambda: defaultdict(float))
decoded = []

def dict_checker(dict1):
    count = 0
    print('len dict1: ', len(dict1.keys()))
    for k, i in dict1.items():
        print('dict1: ' + k, i)


def prob_checker(wl, prob):
    for line in prob:
        for p in line:
            print('wl: ', wl)
            print('prob: ', line, p)


def viterbi(words_line):
    picked_tags = []
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
            if curr_tag in emission_prob.keys():
                if emission_prob[curr_tag].get(f_word) is not None:
                    curr_emission = emission_prob[curr_tag][f_word]
                    prob[i][0] = transition_prob['START'][curr_tag] * curr_emission
                else:
                    prob[i][0] = 0.0
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
                    if tags[j] in emission_prob.keys():
                        if emission_prob[tags[j]].get(words_line[i]) is not None:
                            if transition_prob[tags[p]][tags[j]] == 0.0 or prob[p][i - 1] == 0.0:
                                # print('it was 0')
                                curr_prob = 0.0
                            else:
                                curr_emission = emission_prob[tags[j]][words_line[i]]
                                curr_prob = transition_prob[tags[p]][tags[j]] * prob[p][i - 1] * curr_emission
                        else:
                            # curr_emission = 0.0
                            curr_prob = 0.0
                    else:
                        curr_prob = 0.0

                else:
                    curr_prob = transition_prob[tags[p]][tags[j]] * prob[p][i - 1]

                if max_prob < curr_prob:
                    max_prob = curr_prob
                    index_max_prob = p

            prob[j][i] = max_prob
            backpointer[j][i] = index_max_prob

#     the path starting at state bestpathpointer, that follows backpointer[] to states back in time
    max_prob = -100.0
    index_max_prob = -1

    for i in range(len(tags)):
        # print(len(prob))
        # print(len(prob[0]))
        # print(len(training_words.keys()))
        if max_prob < prob[i][len(words_line) - 1]:
            max_prob = prob[i][len(words_line) - 1]
            index_max_prob = i

    picked_tags.append(tags[index_max_prob])

    for i in range(len(words_line) - 1, 0, -1):
        index_max_prob = backpointer[index_max_prob][i]
        picked_tags.append(tags[index_max_prob])

    picked_tags = picked_tags[::-1]

    return picked_tags


if __name__ == '__main__':
    print('hmmdecode starting main ...')

    input_path = sys.argv[1]
    sentence_words = []
    output_viterbi_tags = []

    with open('hmmmodel.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        training_words = json.loads(lines[0])
        tag_count = json.loads(lines[1])
        emission_prob = json.loads(lines[2])
        transition_prob = json.loads(lines[3])

    print('Starting viterbi ...')

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            words_line = line.strip().split()
            output_viterbi_tags.append(viterbi(words_line))
            sentence_words.append(words_line)

    with open('hmmoutput.txt', 'w', encoding='utf-8') as f:
        for i in range(len(sentence_words)):
            s = ''
            for j in range(len(sentence_words[i])):
                s += sentence_words[i][j] + '/' + output_viterbi_tags[i][j] + ' '
            f.write(s + '\n')
