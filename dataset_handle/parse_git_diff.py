# -*- coding: utf-8 -*-
# modified on sanada's code: https://github.com/tklab-group/UntanglingCommit-sanada 
from git import Repo
import re
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("--repo", dest="repo", required=True)
    parser.add_argument("--commit_file", dest="commit_file", required=True)
    parser.add_argument("--range_dir", dest="range_dir", required=True)
    args = parser.parse_args()

    with open(args.commit_file, 'r') as hash_file:
        content = hash_file.read()
        commit_hashs = content.split('\n')

    repo = Repo(args.repo)

    for commit_hash in commit_hashs:
        if commit_hash == "":
            continue
        repo.git.checkout('-f', commit_hash)
        head = repo.head.commit
        parent = head.parents[0]
        save_commit(repo, head, parent, args.range_dir)
        print('saved commit:' + head.hexsha)

    repo.heads.master.checkout()


def save_commit(repo, head, parent, out_dir):
    # save file name: {commit_hash}_(added/removed).txt
    added_files = []
    removed_files = []
    for diff in parent.diff(head, create_patch=True):
        file_path = diff.a_path or diff.b_path
        if not file_path.endswith('.java'):
            continue
        print(diff.b_path)
        added_chunks, removed_chunks = parse_diff(diff.diff.decode('utf-8'))
        print('ADDED CHUNKS')
        print(added_chunks)
        if len(added_chunks) > 0:
            added_files.append({'path': diff.b_path, 'chunks': added_chunks})
        print('REMOVED CHUNKS')
        print(removed_chunks)
        if len(removed_chunks) > 0:
            removed_files.append({'path': diff.a_path, 'chunks': removed_chunks})

    with open(out_dir + '/' + head.hexsha + '_added.txt', mode='w') as out:
        for added_file in added_files:
            out.write(added_file['path'] + ' ')
            chunk_strs = ['+:' + str(chunk[0]) + ':' + str(chunk[1]) for chunk in added_file['chunks']]
            out.write(','.join(chunk_strs) + '\n')

    with open(out_dir + '/' + head.hexsha + '_removed.txt', mode='w') as out:
        for removed_file in removed_files:
            out.write(removed_file['path'] + ' ')
            chunk_strs = ['-:' + str(chunk[0]) + ':' + str(chunk[1]) for chunk in removed_file['chunks']]
            out.write(','.join(chunk_strs) + '\n')


def parse_diff(diff_str):
    lines = diff_str.split('\n')
    line_iterator = iter(lines)
    added_chunks = []
    removed_chunks = []
    regexp = re.compile(',| ')

    try:
        line = next(line_iterator)
        while True:
            if line.startswith('@@'):
                line_id_strs = [token[1:] for token in regexp.split(line.split('@@')[1]) if token.startswith(('+', '-'))]
                removed_line_id = int(line_id_strs[0])
                added_line_id = int(line_id_strs[1])
                line = next(line_iterator)
            elif line.startswith('+'):
                chunk_start = added_line_id
                try:
                    while line.startswith('+'):
                        line = next(line_iterator)
                        added_line_id += 1
                except StopIteration:
                    added_chunks.append((chunk_start, added_line_id))
                    break
                added_chunks.append((chunk_start, added_line_id - 1))
            elif line.startswith('-'):
                chunk_start = removed_line_id
                try:
                    while line.startswith('-'):
                        line = next(line_iterator)
                        removed_line_id += 1
                except StopIteration:
                    removed_chunks.append((chunk_start, removed_line_id))
                    break
                removed_chunks.append((chunk_start, removed_line_id - 1))
            else:
                line = next(line_iterator)
                added_line_id += 1
                removed_line_id += 1

    except StopIteration:
        pass

    return (added_chunks, removed_chunks)


if __name__ == '__main__':
    main()
