import sys, os, json

if __name__ == '__main__':
    print('Starting main ...')

    input_path = sys.argv[1]
    output_file = 'hmmscore.txt'

    with open('hmmmodel.txt', 'r', encoding='utf-8') as f1:
        lines = f1.readlines()
        training_words = json.loads(lines[0])
        tag_count = json.loads(lines[1])
        emission_prob = json.loads(lines[2])
        transition_prob = json.loads(lines[3])



    output_file = 'hmmscore.txt'


