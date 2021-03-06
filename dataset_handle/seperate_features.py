import os
from argparse import ArgumentParser


def seperate_features(feature_file_path, out_file_path):
    with open(feature_file_path, 'r') as range_file:
        content = range_file.read()
        chunks = content.split('/t/')

    i = 1
    out_files = []
    for chunk in chunks:
        if chunk == "" or chunk == " " or chunk == "\n":
            continue
        output_file = out_file_path + "_" + str(i) + ".txt"
        raw_feature_file = feature_file_path.split('.')[0] + '_' + str(i) + '.txt'
        out_files.append(output_file)
        i += 1
        with open(output_file, 'w') as out_file, \
                open(raw_feature_file, 'w') as raw_file:
            out_file.write(chunk.split('/f/')[1])
            raw_file.write(chunk)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("-commitfile", "--commit_file", dest="commit_file", required=True)
    parser.add_argument("--feature_dir", dest="feature_dir", required=True)
    parser.add_argument("--out_dir", dest="out_dir", required=True)
    args = parser.parse_args()

    with open(args.commit_file, 'r') as hash_file:
        content = hash_file.read()
        commits = content.split('\n')

    for commit in commits:
        if commit == "":
            continue
        feature_file_path = args.feature_dir + '/' + commit + '_added.txt'
        out_file_path = args.out_dir + '/' + commit + '_added'
        if os.path.exists(feature_file_path):
            seperate_features(feature_file_path, out_file_path)
            os.remove(feature_file_path)
        else:
            print('Seperate features: no such file:' + feature_file_path)

        feature_file_path = args.feature_dir + '/' + commit + '_removed.txt'
        out_file_path = args.out_dir + '/' + commit + '_removed'
        if os.path.exists(feature_file_path):
            seperate_features(feature_file_path, out_file_path)
            os.remove(feature_file_path)
        else:
            print('Seperate features: no such file:' + feature_file_path)
