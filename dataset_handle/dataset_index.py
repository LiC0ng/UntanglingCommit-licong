import os
from argparse import ArgumentParser
from itertools import combinations


def untangled_index(dictt, untangled_commits, output_path, feature_path):
    with open(output_path + '/true/ins.txt', 'w') as ins_file, \
            open(output_path + '/true/ino.txt', 'w') as ino_file, \
            open(output_path + '/true/its.txt', 'w') as its_file, \
            open(output_path + '/true/ito.txt', 'w') as ito_file:
        for commit in untangled_commits:
            if commit == "" or commit == " " or commit == "\n":
                continue
            untangled_chunk_pairs = combinations(dictt[commit], 2)
            for pair in untangled_chunk_pairs:
                with open(feature_path + '/' + pair[0]) as feature1_file, \
                        open(feature_path + '/' + pair[1]) as feature2_file:
                    feature1 = feature1_file.read()
                    feature2 = feature2_file.read()
                    if(feature1.split('/f/')[0] == feature2.split('/f/')[0]):
                        if ((pair[0].find('added') > 0
                             and pair[1].find('added') > 0)
                                or (pair[0].find('removed') > 0
                                    and pair[1].find('removed') > 0)):
                            ins_file.writelines(pair[0] + '\t' + pair[1] +
                                                '\t' + '1\n')
                        else:
                            ino_file.writelines(pair[0] + '\t' + pair[1] +
                                                '\t' + '1\n')
                    else:
                        if ((pair[0].find('added') > 0
                             and pair[1].find('added') > 0)
                                or (pair[0].find('removed') > 0
                                    and pair[1].find('removed') > 0)):
                            its_file.writelines(pair[0] + '\t' + pair[1] +
                                                '\t' + '1\n')
                        else:
                            ito_file.writelines(pair[0] + '\t' + pair[1] +
                                                '\t' + '1\n')


def tangled_index(dictt, tangled_commits, output_path, feature_path):
    with open(output_path + '/false/ins.txt', 'w') as ins_file, \
            open(output_path + '/false/ino.txt', 'w') as ino_file, \
            open(output_path + '/false/its.txt', 'w') as its_file, \
            open(output_path + '/false/ito.txt', 'w') as ito_file:
        for commit in tangled_commits:
            if commit == "" or commit == " " or commit == "\n":
                continue
            commit_pair = commit.split(' ')
            feature_list1 = dictt[commit_pair[0]]
            feature_list2 = dictt[commit_pair[1]]
            for feature_file1 in feature_list1:
                for feature_file2 in feature_list2:
                    with open(feature_path + '/' + feature_file1) as feature1_file, \
                            open(feature_path + '/' + feature_file2) as feature2_file:
                        feature1 = feature1_file.read()
                        feature2 = feature2_file.read()
                        if(feature1.split('/f/')[0] == feature2.split('/f/')[0]):
                            if ((feature_file1.find('added') > 0
                                 and feature_file2.find('added') > 0)
                                    or (feature_file1.find('remove') > 0
                                        and feature_file2.find('remove') > 0)):
                                ins_file.writelines(feature_file1 + '\t' +
                                                    feature_file2 + '\t' +
                                                    '-1\n')
                            else:
                                ino_file.writelines(feature_file1 + '\t' +
                                                    feature_file2 + '\t' +
                                                    '-1\n')
                        else:
                            if ((feature_file1.find('added') > 0
                                 and feature_file2.find('added') > 0)
                                    or (feature_file1.find('remove') > 0
                                        and feature_file2.find('remove') > 0)):
                                its_file.writelines(feature_file1 + '\t' +
                                                    feature_file2 + '\t' +
                                                    '-1\n')
                            else:
                                ito_file.writelines(feature_file1 + '\t' +
                                                    feature_file2 + '\t' +
                                                    '-1\n')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-data_dir", "--data_dir", dest="data_dir", required=True)
    parser.add_argument("--index_dir", dest="index_dir", required=True)
    parser.add_argument("--feature_dir0", dest="feature_dir", required=True)
    parser.add_argument("-out_dir", "--out_dir", dest="out_dir", required=True)
    args = parser.parse_args()

    dictt = {}
    untangled_commit_file = args.data_dir + '/' + 'true.csv'
    tangled_commit_file = args.data_dir + '/' + 'false.csv'
    with open(untangled_commit_file, 'r') as hash_file:
        content = hash_file.read()
        untangled_commits = content.split('\n')

    with open(tangled_commit_file, 'r') as hash_file:
        content = hash_file.read()
        tangled_commits = content.split('\n')

    for commit in untangled_commits:
        if commit == "" or commit == " " or commit == "\n":
            continue
        dictt[commit] = []

    files_list = os.listdir(args.feature_dir)
    for file in files_list:
        commit = file.split("_")[0]
        if commit in dictt.keys():
            dictt[commit].append(file)

    untangled_index(dictt, untangled_commits, args.out_dir, args.feature_dir)
    tangled_index(dictt, tangled_commits, args.out_dir, args.feature_dir)
