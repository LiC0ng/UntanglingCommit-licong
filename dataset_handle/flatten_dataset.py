import random
import os
from argparse import ArgumentParser

def flatten_file(path):
    with open(path, 'r') as input_file:
        true_datas = []
        false_datas = []
        for line in input_file:
            line = line.rstrip('\n')
            if line.split(' ')[0] == '1':
                true_datas.append(line)
            elif line.split(' ')[0] == '0':
                false_datas.append(line)

    sample_num = min(len(true_datas), len(false_datas))
    true_datas = random.sample(true_datas, sample_num)
    false_datas = random.sample(false_datas, sample_num)

    with open(path[:-4] + '_flattened.csv', 'w') as output_file:
        for data in true_datas:
            output_file.write('{}\n'.format(data))

        for data in false_datas:
            output_file.write('{}\n'.format(data))


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", dest="input_path", required=True)
    args = parser.parse_args()

    if os.path.isfile(args.input_path):
        flatten_file(args.input_path)
    elif os.path.isdir(args.input_path):
        for file_path in os.listdir(args.input_path):
            flatten_file(args.input_path + '/' + file_path)

    print('done')
