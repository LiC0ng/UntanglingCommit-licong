# -*- coding: utf-8 -*-
from git import Repo
import os
import itertools
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("-r", dest="repo", required=True)
    parser.add_argument("-i", dest="input_path", required=True)
    parser.add_argument("-o", dest="output_path", required=True)
    args = parser.parse_args()

    repo = Repo(args.repo)

    commit_datas = []
    with open(args.input_path, 'r') as input_file:
        for line in input_file:
            commit_hash = line.rstrip('\n')
            commit = repo.commit(commit_hash)
            commit_datas.append({
                'hash': commit_hash,
                'author_name': commit.author.name,
                'author_email': commit.author.email,
                'datetime': commit.authored_datetime,
                'files': commit.stats.files.keys()
                })

    tangled_list = []
    for pair in itertools.combinations(commit_datas, 2):
        delta_date = pair[0]['datetime'] - pair[1]['datetime']
        if abs(delta_date.days) > 14:
            continue

        files0 = pair[0]['files']
        files1 = pair[1]['files']
        is_apart = True
        for file0 in files0:
            for file1 in files1:
                common_path = os.path.commonpath([file0, file1])
                subpath0 = file0.replace(common_path, '', 1)
                subpath1 = file1.replace(common_path, '', 1)
                dist0 = len(subpath0.split('/'))
                dist1 = len(subpath1.split('/'))
                if dist0 <= 4 and dist1 <= 4:
                    is_apart = False
        if is_apart:
            continue

        tangled_list.append(pair)

    with open(args.output_path, 'w') as output_file: #, open(args.output_path + '.info', 'w') as info_file:
        for pair in tangled_list:
            output_file.write('{} {}\n'.format(pair[0]['hash'], pair[1]['hash']))
            '''
            info_file.write(str(pair[0]))
            info_file.write('\n')
            info_file.write(str(pair[1]))
            info_file.write('\n')
            info_file.write('\n')
            '''

    print('done')

if __name__ == '__main__':
    main()
