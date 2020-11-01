import random
import itertools
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", dest="source_path", required=True)
    parser.add_argument("-t", dest="tangle_path", required=True)
    parser.add_argument("-o", dest="output_dir", required=True)
    args = parser.parse_args()

    with open(args.source_path, 'r') as input_file:
        all_commits = set()
        for line in input_file:
            all_commits.add(line.rstrip('\n'))

    with open(args.tangle_path, 'r') as input_file:
        test_commits = set()
        for line in input_file:
            pair = line.rstrip('\n').split(' ')
            test_commits.add(pair[0])
            test_commits.add(pair[1])

    train_path = args.output_dir + '/train.csv'
    test_path = args.output_dir + '/test.csv'

    with open(train_path, 'w') as train_file:
        train_commits = all_commits - test_commits
        for commit in train_commits:
            text = '{}\n'.format(commit)
            train_file.write(text)

    with open(test_path, 'w') as test_file:
        for commit in test_commits:
            text = '{}\n'.format(commit)
            test_file.write(text)

    print('done')
