import os
from argparse import ArgumentParser


def create_dict_with_id(feature_path, dict_path):
    dictt = set()
    files_list = os.listdir(feature_path)
    for file in files_list:
        feature_file = open(feature_path + '/' + file, 'r')
        feature = feature_file.read()
        words = feature.split('"')
        for word in words:
            if word.find('[') >= 0 or word.find(':') >= 0 or word.find('{') >= 0 or word.find(',') >= 0:
                continue
            dictt.add(word)
        feature_file.close()

    dict_file = open(dict_path + '/withid.txt', 'w')
    for word in dictt:
        dict_file.write(word + " ")
    dict_file.close()


def create_dict_without_id(feature_path, dict_path):
    dictt = set()
    files_list = os.listdir(feature_path)
    for file in files_list:
        feature_file = open(feature_path + '/' + file, 'r')
        feature = feature_file.read()
        words = feature.split('"')
        for word in words:
            if word.find('NameExpr_') >= 0 or word.find('[') >= 0 or word.find(':') >= 0 or word.find('{') >= 0 or word.find(',') >= 0:
                continue
            dictt.add(word)
        feature_file.close()

    dict_file = open(dict_path + '/nodetype.txt', 'w')
    for word in dictt:
        dict_file.write(word + " ")
    dict_file.close()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--feature_dir", dest="feature_dir", required=True)
    parser.add_argument("--dict_dir", dest="dict_dir", required=True)
    args = parser.parse_args()
    dict_path = args.dict_dir
    feature_path = args.feature_dir + '/features1'
    create_dict_with_id(feature_path, dict_path)
    feature_path = args.feature_dir + '/features2'
    create_dict_without_id(feature_path, dict_path)
