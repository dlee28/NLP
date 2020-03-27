import sys, os

tag_list =[] #store the word/tag in the input_file

def read_training_data(input_path):
    with open(input_path, 'r', encoding='utf-8') as input_file:
        for line in input_file:
            # input file will be structured to have word/tag and a new sentence per new line.
            for word_tag in line.strip().split():
                tag_list.append(word_tag.rsplit('/'))


if __name__ == '__main__':
    print('Starting main ...')

    # path to a single file with training data
    input_path = sys.argv[1]

    # read training data
    read_training_data(input_path)
