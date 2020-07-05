#!/usr/bin/python

import os
import sys
import subprocess
from threading import Timer
from argparse import ArgumentParser
from subprocess import Popen, PIPE
from git import Repo


# range_file_pathをわたして、１コミットぶんの特徴をまるまる抽出するjavaコマンドを実行
def extract_on_head_commit(args, range_file_path, feature_file_path):
    # chunk_fileの中を見れば、変更があったファイルpath一覧がある。
    command = ['java', '-cp', args.jar, 'JavaExtractor.App',
               '--max_path_length', str(args.max_path_length),
               '--max_path_width', str(args.max_path_width),
               '--num_threads', str(args.num_threads),
               '--repo', str(args.repo),
               '--chunk_file', range_file_path,
               '--with_id', '0']

    # print command
    # os.system(command)
    kill = lambda process: process.kill()
    failed = False
    with open(feature_file_path, 'w') as outputFile:
        sleeper = subprocess.Popen(command, stdout=outputFile, stderr=subprocess.PIPE)
        timer = Timer(600000, kill, [sleeper])

        try:
            timer.start()
            stdout, stderr = sleeper.communicate()
        finally:
            timer.cancel()

        if sleeper.poll() == 0:
            if len(stderr) > 0:
                print(sys.stderr, stderr, file=sys.stdout)
        else:
            print(sys.stderr, feature_file_path + ' was not completed in time', file=sys.stdout)
            failed = True
    if failed:
        if os.path.exists(feature_file_path):
            os.remove(feature_file_path)


# range_file_pathをわたして、１コミットぶんの特徴をまるまる抽出するjavaコマンドを実行
def extract_on_head_commit_with_id(args, range_file_path, feature_file_path):
    # chunk_fileの中を見れば、変更があったファイルpath一覧がある。
    command = ['java', '-cp', args.jar, 'JavaExtractor.App',
               '--max_path_length', str(args.max_path_length),
               '--max_path_width', str(args.max_path_width),
               '--num_threads', str(args.num_threads),
               '--repo', str(args.repo),
               '--chunk_file', range_file_path,
               '--with_id', '1']

    # print command
    # os.system(command)
    kill = lambda process: process.kill()
    failed = False
    with open(feature_file_path, 'w') as outputFile:
        sleeper = subprocess.Popen(command, stdout=outputFile, stderr=subprocess.PIPE)
        timer = Timer(600000, kill, [sleeper])

        try:
            timer.start()
            stdout, stderr = sleeper.communicate()
        finally:
            timer.cancel()

        if sleeper.poll() == 0:
            if len(stderr) > 0:
                print(sys.stderr, stderr, file=sys.stdout)
        else:
            print(sys.stderr, feature_file_path + ' was not completed in time', file=sys.stdout)
            failed = True
    if failed:
        if os.path.exists(feature_file_path):
            os.remove(feature_file_path)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-maxlen", "--max_path_length", dest="max_path_length", required=False, default=8)
    parser.add_argument("-maxwidth", "--max_path_width", dest="max_path_width", required=False, default=2)
    parser.add_argument("-threads", "--num_threads", dest="num_threads", required=False, default=64)
    parser.add_argument("-j", "--jar", dest="jar", required=True)
    parser.add_argument("-repo", "--repo", dest="repo", required=True)
    parser.add_argument("-commitfile", "--commit_file", dest="commit_file", required=True)
    parser.add_argument("--range_dir", dest="range_dir", required=True)
    parser.add_argument("--feature_dir0", dest="feature_dir0", required=True)
    parser.add_argument("--feature_dir1", dest="feature_dir1", required=True)
    args = parser.parse_args()

    with open(args.commit_file, 'r') as hash_file:
        content = hash_file.read()
        commits = content.split('\n')

    repo = Repo(args.repo)

    for commit in commits:
        if commit == "":
            continue
        repo.git.checkout('-f', commit)
        range_file_path = args.range_dir + '/' + commit + '_added.txt'
        feature_file_path0 = args.feature_dir0 + '/' + commit + '_added.txt'
        extract_on_head_commit(args, range_file_path, feature_file_path0)
        feature_file_path1 = args.feature_dir1 + '/' + commit + '_added.txt'
        extract_on_head_commit_with_id(args, range_file_path, feature_file_path1)

        repo.git.checkout('-f', repo.head.commit.parents[0].hexsha)
        range_file_path = args.range_dir + '/' + commit + '_removed.txt'
        feature_file_path0 = args.feature_dir0 + '/' + commit + '_removed.txt'
        extract_on_head_commit(args, range_file_path, feature_file_path0)
        feature_file_path1 = args.feature_dir1 + '/' + commit + '_removed.txt'
        extract_on_head_commit_with_id(args, range_file_path, feature_file_path1)

    repo.heads.master.checkout('-f')
