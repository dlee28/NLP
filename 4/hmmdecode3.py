import sys, os, json
from collections import defaultdict

training_words = defaultdict(float)
tag_count = defaultdict(float)
emission_prob = defaultdict(lambda: defaultdict(float))
transition_prob = defaultdict(lambda: defaultdict(float))
decoded = []

def viterbi(sentence_words):
    tag = []


if __name__ == '__main__':
    print('Starting main ...')

    input_path = sys.argv[1]

    with open('hmmmodel.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        training_words = json.loads(lines[0])
        tag_count = json.loads(lines[1])
        emission_prob = json.loads(lines[2])
        transition_prob = json.loads(lines[3])

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            line_words = line.strip().split()




    output_file = 'hmmscore.txt'


