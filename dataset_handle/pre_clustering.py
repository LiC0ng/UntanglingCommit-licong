import random
from argparse import ArgumentParser
import itertools
import os

'''
This script preprocesses the data from MethodPaths. It truncates methods with too many contexts,
and pads methods with less paths with spaces.
'''


def process_file(in_path, out_path, max_tokens):
    sum_total = 0
    sum_sampled = 0
    total = 0
    empty = 0
    max_unfiltered = 0
    with open(out_path, 'w') as out_file, open(in_path, 'r') as in_file:
        for line in in_file:
            strs = line.rstrip('\n').split(" ")
            label = strs[0]
            chunks = [chunk_str.split(",") for chunk_str in strs[1:3]]
            replace_shared_identifier(chunks[0], chunks[1])
            padded = []
            for tokens in chunks:
                if len(tokens) > max_unfiltered:
                    max_unfiltered = len(tokens)
                sum_total += len(tokens)

                if len(tokens) > max_tokens:
                    trim = (len(tokens) - max_tokens) // 2
                    tokens = tokens[trim:-trim-1]

                if len(tokens) == 0:
                    empty += 1
                    continue

                sum_sampled += len(tokens)

                csv_padding = "," * (max_tokens - len(tokens))
                padded.append(",".join(tokens) + csv_padding)

            padded = [label] + padded + strs[3:]
            out_file.write(" ".join(padded) + '\n')
            total += 1

    if total == 0:
        return

    print('File: ' + in_path)
    print('Average total tokens: ' + str(float(sum_total) / total / 2))
    print('Average final (after sampling) tokens: ' + str(float(sum_sampled) / total / 2))
    print('Total examples: ' + str(total))
    print('Empty examples: ' + str(empty))
    print('Max number of tokens per word: ' + str(max_unfiltered))
    return total


def replace_shared_identifier(tokens1, tokens2):
    identifier_to_index = {}
    for index, token in enumerate(tokens1):
        if token[1:].startswith("NameExpr_"):
            identifier = token.split("_")[1]
            if identifier in identifier_to_index:
                identifier_to_index[identifier].append(index)
            else:
                identifier_to_index[identifier] = [index]

    should_replace = set()
    for index, token in enumerate(tokens2):
        if token[1:].startswith("NameExpr_"):
            identifier = token.split("_")[1]
            if identifier in identifier_to_index:
                should_replace.add(identifier)
                tokens2[index] = tokens2[index][0] + "NameExpr_shared"
            else:
                tokens2[index] = tokens2[index][0] + "NameExpr"

    for identifier, indices in identifier_to_index.items():
        if identifier in should_replace:
            for index in indices:
                tokens1[index] = tokens1[index][0] + "NameExpr_shared"
        else:
            for index in indices:
                tokens1[index] = tokens1[index][0] + "NameExpr"


def load_from_token_file(file_path):
    chunk_dict = {}
    with open(file_path, 'r') as input_file:
        for line in input_file:
            strs = line.rstrip('\n').split(" ")
            path = strs[0]
            chunks = strs[1:]
            chunk_dict[path] = chunks

    return chunk_dict


def write_chunk_pairs(shared_path_file, unshared_path_file, dict1, dict2, commit1, commit2, sign1, sign2, label, commit_pair_id):
    for path1 in dict1.keys():
        for path2 in dict2.keys():
            if path1 == path2:
                for chunk_id1, chunk1 in enumerate(dict1[path1]):
                    for chunk_id2, chunk2 in enumerate(dict2[path2]):
                        data_text = '{} {} {}'.format(label, chunk1, chunk2)
                        info_text = '{0} {1}_{2}_{3}{4} {5}_{6}_{7}{8}'.format(
                            commit_pair_id, commit1, path1, sign1, chunk_id1, commit2, path2, sign2, chunk_id2)
                        shared_path_file.write('{} {}\n'.format(data_text, info_text))
            else:
                for chunk_id1, chunk1 in enumerate(dict1[path1]):
                    for chunk_id2, chunk2 in enumerate(dict2[path2]):
                        data_text = '{} {} {}'.format(label, chunk1, chunk2)
                        info_text = '{0} {1}_{2}_{3}{4} {5}_{6}_{7}{8}'.format(
                            commit_pair_id, commit1, path1, sign1, chunk_id1, commit2, path2, sign2, chunk_id2)
                        unshared_path_file.write('{} {}\n'.format(data_text, info_text))


def load_true_data(commit_file_path, token_data_dir, out_dir, commit_pair_id):
    inner_same_path = out_dir + '/inner_same.c2v'
    inner_opp_path = out_dir + '/inner_opposite.c2v'
    inter_same_path = out_dir + '/inter_same.c2v'
    inter_opp_path = out_dir + '/inter_opposite.c2v'

    with open(commit_file_path) as commit_file, \
            open(inner_same_path, 'a') as inner_same_file, open(inner_opp_path, 'a') as inner_opp_file, \
            open(inter_same_path, 'a') as inter_same_file, open(inter_opp_path, 'a') as inter_opp_file:
        for commit in commit_file:
            commit = commit.rstrip('\n')

            added_token_file_path = token_data_dir + '/' + commit + '_added.txt'
            added_dict = load_from_token_file(added_token_file_path)

            removed_token_file_path = token_data_dir + '/' + commit + '_removed.txt'
            removed_dict = load_from_token_file(removed_token_file_path)

            for path, chunks in added_dict.items():
                for chunk_info1, chunk_info2 in itertools.combinations(enumerate(chunks), 2):
                    chunk_id1, chunk1 = chunk_info1
                    chunk_id2, chunk2 = chunk_info2
                    data_text = '{} {} {}'.format(1, chunk1, chunk2)
                    info_text = '{0} {1}_{2}_+{3} {1}_{2}_+{4}'.format(
                        commit_pair_id, commit, path, chunk_id1, chunk_id2)
                    inner_same_file.write('{} {}\n'.format(data_text, info_text))
            for path, chunks in removed_dict.items():
                for chunk_info1, chunk_info2 in itertools.combinations(enumerate(chunks), 2):
                    chunk_id1, chunk1 = chunk_info1
                    chunk_id2, chunk2 = chunk_info2
                    data_text = '{} {} {}'.format(1, chunk1, chunk2)
                    info_text = '{0} {1}_{2}_-{3} {1}_{2}_-{4}'.format(
                        commit_pair_id, commit, path, chunk_id1, chunk_id2)
                    inner_same_file.write('{} {}\n'.format(data_text, info_text))
            for path1, path2 in itertools.combinations(added_dict.keys(), 2):
                for chunk_id1, chunk1 in enumerate(added_dict[path1]):
                    for chunk_id2, chunk2 in enumerate(added_dict[path2]):
                        data_text = '{} {} {}'.format(1, chunk1, chunk2)
                        info_text = '{0} {1}_{2}_+{3} {1}_{4}_+{5}'.format(
                            commit_pair_id, commit, path1, chunk_id1, path2, chunk_id2)
                        inter_same_file.write('{} {}\n'.format(data_text, info_text))
            for path1, path2 in itertools.combinations(removed_dict.keys(), 2):
                for chunk_id1, chunk1 in enumerate(removed_dict[path1]):
                    for chunk_id2, chunk2 in enumerate(removed_dict[path2]):
                        data_text = '{} {} {}'.format(1, chunk1, chunk2)
                        info_text = '{0} {1}_{2}_-{3} {1}_{4}_-{5}'.format(
                            commit_pair_id, commit, path1, chunk_id1, path2, chunk_id2)
                        inter_same_file.write('{} {}\n'.format(data_text, info_text))
            write_chunk_pairs(inner_opp_file, inter_opp_file,
                added_dict, removed_dict, commit, commit, '+', '-', 1, commit_pair_id)


def load_false_data(commit_file_path, token_data_dir, out_dir, commit_pair_id):
    inner_same_path = out_dir + '/inner_same.c2v'
    inner_opp_path = out_dir + '/inner_opposite.c2v'
    inter_same_path = out_dir + '/inter_same.c2v'
    inter_opp_path = out_dir + '/inter_opposite.c2v'

    with open(commit_file_path) as commit_file, \
            open(inner_same_path, 'a') as inner_same_file, open(inner_opp_path, 'a') as inner_opp_file, \
            open(inter_same_path, 'a') as inter_same_file, open(inter_opp_path, 'a') as inter_opp_file:
        for commits in commit_file:
            commits = commits.rstrip('\n').split(" ")

            added_token_file_path1 = token_data_dir + '/' + commits[0] + '_added.txt'
            added_dict1 = load_from_token_file(added_token_file_path1)

            removed_token_file_path1 = token_data_dir + '/' + commits[0] + '_removed.txt'
            removed_dict1 = load_from_token_file(removed_token_file_path1)

            added_token_file_path2 = token_data_dir + '/' + commits[1] + '_added.txt'
            added_dict2 = load_from_token_file(added_token_file_path2)

            removed_token_file_path2 = token_data_dir + '/' + commits[1] + '_removed.txt'
            removed_dict2 = load_from_token_file(removed_token_file_path2)

            write_chunk_pairs(inner_same_file, inter_same_file,
                added_dict1, added_dict2, commits[0], commits[1], '+', '+', 0, commit_pair_id)
            write_chunk_pairs(inner_same_file, inter_same_file,
                removed_dict1, removed_dict2, commits[0], commits[1], '-', '-', 0, commit_pair_id)
            write_chunk_pairs(inner_opp_file, inter_opp_file,
                added_dict1, removed_dict2, commits[0], commits[1], '+', '-', 0, commit_pair_id)
            write_chunk_pairs(inner_opp_file, inter_opp_file,
                added_dict2, removed_dict1, commits[1], commits[0], '+', '-', 0, commit_pair_id)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-i", "--input_dir", dest="input_dir",
                        help="input directory represents artificially composite commit", required=True)
    parser.add_argument("-o", "--output_dir", dest="output_dir",
                        help="output directory includes subdirectory", metavar="FILE", required=True)
    parser.add_argument("-cpi", "--commit_pair_id", dest="commit_pair_id",
                        help="identification of project name and commit pair", required=True)
    parser.add_argument("-tkd", "--token_data_dir", dest="token_data_dir",
                        help="path to token data directory", required=True)
    parser.add_argument("-mc", "--max_tokens", dest="max_tokens", default=200,
                        help="number of max tokens to keep", required=False)
    args = parser.parse_args()

    true_data_path = args.input_dir + '/true.csv'
    false_data_path = args.input_dir + '/false.csv'
    if not os.path.exists(true_data_path) or not os.path.exists(false_data_path):
        print('skipped.  commit list does not exist: ' + args.input_dir)
        exit()

    intermediate_dir = '{}/unpadded'.format(args.output_dir)

    load_true_data(commit_file_path=true_data_path, token_data_dir=args.token_data_dir, out_dir=intermediate_dir, commit_pair_id=args.commit_pair_id)
    load_false_data(commit_file_path=false_data_path, token_data_dir=args.token_data_dir, out_dir=intermediate_dir, commit_pair_id=args.commit_pair_id)

    intermediate_files = [f for f in os.listdir(intermediate_dir) if f.endswith('.c2v')]
    out_dir = '{}/padded'.format(args.output_dir)

    for intermediate_file in intermediate_files:
        intermediate_path = intermediate_dir + '/' + intermediate_file
        out_path = out_dir + '/' + intermediate_file
        num_examples = process_file(in_path=intermediate_path, out_path=out_path,
                                    max_tokens=int(args.max_tokens))
