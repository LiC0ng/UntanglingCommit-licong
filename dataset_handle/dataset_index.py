import os
from argparse import ArgumentParser
from itertools import combinations


def untangled_index(dictt, commits, index_path):
    with open(index_path, 'w') as index_file:
        for commit in commits:
            if commit == 0:
                continue
            features_of_commit = combinations(dictt[commit], 2)
            for feature in features_of_commit:
                index_file.writelines(feature[0] + '\t' + feature[1] + '\t' + '1\n')


def tangled_index(dictt, tangled_file, index_path):
    with open(tangled_file, 'r') as input_file, \
            open(index_path, 'w') as index_file:
        for line in input_file:
            pair = line.rstrip('\n').split(' ')
            feature_list1 = dictt[pair[0]]
            feature_list2 = dictt[pair[1]]
            for feature_1 in feature_list1:
                for feature_2 in feature_list2:
                    index_file.writelines(feature_1 + '\t' + feature_2 + '\t' + '-1\n')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-commitfile", "--commit_file", dest="commit_file", required=True)
    parser.add_argument("-tangledfile", "--tangled_file", dest="tangled_file", required=True)
    parser.add_argument("--index_dir", dest="index_dir", required=True)
    parser.add_argument("--feature_dir0", dest="feature_dir", required=True)
    args = parser.parse_args()

    dictt = {}
    with open(args.commit_file, 'r') as hash_file:
        content = hash_file.read()
        commits = content.split('\n')

    for commit in commits:
        if commit == 0:
            continue
        dictt[commit] = []

    files_list = os.listdir(args.feature_dir)
    for file in files_list:
        commit = file.split("_")[0]
        dictt[commit].append(file)

    index_path = args.index_dir + '/untangled.txt'
    untangled_index(dictt, commits, index_path)

    index_path = args.index_dir + '/tangled.txt'
    tangled_index(dictt, args.tangled_file, index_path)
