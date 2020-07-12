from argparse import ArgumentParser
import random


def ReadFileDatas(index_path):
    FileNamelist = []
    file = open(index_path, 'r')
    for line in file:
        if line == "" or line == " ":
            continue
        FileNamelist.append(line)
    print('len ( FileNamelist ) = ', len(FileNamelist))
    file.close()
    return FileNamelist


def WriteDatasToFile(listInfo, data_path, repo):
    train_data = open(data_path + '/traindata.txt', mode='a')
    dev_data = open(data_path + '/devdata.txt', mode='a')
    test_data = open(data_path + '/totaltest.txt', mode='a')
    fixed_data = open(data_path + '/' + repo + '_test.txt', mode='w')
    for idx in range(len(listInfo)):
        if idx <= (len(listInfo) * 8 / 10):
            train_data.write(listInfo[idx])
        elif idx > (len(listInfo) * 8 / 10) and idx <= (len(listInfo) * 9 / 10):
            dev_data.write(listInfo[idx])
        else:
            test_data.write(listInfo[idx])
            fixed_data.write(listInfo[idx])
    train_data.close()
    dev_data.close()
    test_data.close()
    fixed_data.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--source_dir", dest="source_dir", required=True)
    parser.add_argument("--dest_dir", dest="dest_dir", required=True)
    parser.add_argument("--repo", dest="repo", required=True)
    args = parser.parse_args()

    tangled_list = ReadFileDatas(args.source_dir + '/tangled.txt')
    random.shuffle(tangled_list)
    untangled_list = ReadFileDatas(args.source_dir + '/untangled.txt')
    random.shuffle(untangled_list)
    max_len = len(tangled_list) if len(tangled_list) < len(untangled_list) else len(untangled_list)
    tangled_list = tangled_list[0: max_len]
    untangled_list = untangled_list[0: max_len]

    WriteDatasToFile(tangled_list, args.dest_dir, args.repo)
    WriteDatasToFile(untangled_list, args.dest_dir, args.repo)
