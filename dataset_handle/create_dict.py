import os


def create_dict_with_id(feature_path):
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

    dict_file = open('dataset/dict/withid.txt', 'w')
    for word in dictt:
        dict_file.write(word + " ")
    dict_file.close()


def create_dict_without_id(feature_path):
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

    dict_file = open('dataset/dict/noid.txt', 'w')
    for word in dictt:
        dict_file.write(word + " ")
    dict_file.close()


if __name__ == '__main__':
    feature_path = 'dataset/features/features1'
    create_dict_with_id(feature_path)
    feature_path = 'dataset/features/features2'
    create_dict_without_id(feature_path)
