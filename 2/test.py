import sys
import os
from collections import defaultdict

if __name__ == '__main__':

    print('Starting main ...')

    input_path = sys.argv[1]

    positive_deceptive = []
    positive_truthful = []
    negative_deceptive = []
    negative_truthful = []

    training_data = defaultdict(list)
    # print(type(training_data))

    for root, dirs, files in os.walk(input_path):
        if len(dirs) == 0:
            print(root, dirs, files)

