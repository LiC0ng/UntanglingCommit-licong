import random
from argparse import ArgumentParser


def ReadFileDatas(index_path):
    FileNamelist = []
    file = open(index_path + '/dataset.txt', 'r')
    for line in file:
        FileNamelist.append(line)
    print('len ( FileNamelist ) = ', len(FileNamelist))
    file.close()
    return FileNamelist


def WriteDatasToFile(listInfo, data_path):
    train_data = open(data_path + '/traindata.txt', mode='w')
    dev_data = open(data_path + '/devdata.txt', mode='w')
    test_data = open(data_path + '/testdata.txt', mode='w')
    for idx in range(len(listInfo)):
        if idx < (len(listInfo) * 8 / 10):
            train_data.write(listInfo[idx])
        elif idx >= (len(listInfo) * 8 / 10) and idx < (len(listInfo) * 9 / 10):
            dev_data.write(listInfo[idx])
        else:
            test_data.write(listInfo[idx])
    train_data.close()
    dev_data.close()
    test_data.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--index_dir", dest="index_dir", required=True)
    parser.add_argument("--data_dir", dest="data_dir", required=True)
    args = parser.parse_args()
    listFileInfo = ReadFileDatas(args.index_dir)
    # shuffle dataset
    random.shuffle(listFileInfo)
    WriteDatasToFile(listFileInfo, args.data_dir)
