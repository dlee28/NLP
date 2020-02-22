import sys, os
from _collections import defaultdict



if __name__ == '__main__':

    print('Starting main ...')

    input_path = sys.argv[1]

    training_data = defaultdict(list)
    print('reading training data ...')
    for root, dirs, files in os.walk(input_path):
        if len(dirs) == 0:
            #root.endswith('4') or root.endswith('2') or root.endswith('3'):
            # or root.endswith('1') or root.endswith('2') or root.endswith('3')
            # print(root)
            for file in files:
                if root.rfind('positive') >= 0 and root.rfind('deceptive') >= 0:
                    training_data['positive_deceptive'].append(root + '/' + file)
                elif root.rfind('positive') >= 0 and root.rfind('truthful') >= 0:
                    training_data['positive_truthful'].append(root + '/' + file)
                elif root.rfind('negative') >= 0 and root.rfind('deceptive') >= 0:
                    training_data['negative_deceptive'].append(root + '/' + file)
                elif root.rfind('negative') >= 0 and root.rfind('truthful') >= 0:
                    training_data['negative_truthful'].append(root + '/' + file)
    print('finished reading training data ...')

    print('end main ...')