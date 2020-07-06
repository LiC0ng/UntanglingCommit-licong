import random


def ReadFileDatas():
    FileNamelist = []
    file = open('dataset/index/dataset.txt', 'r')
    for line in file:
        FileNamelist.append(line)
    print('len ( FileNamelist ) = ', len(FileNamelist))
    file.close()
    return FileNamelist


def WriteDatasToFile(listInfo):
    train_data = open('dataset/dataset/traindata.txt', mode='w')
    dev_data = open('dataset/dataset/devdata.txt', mode='w')
    test_data = open('dataset/dataset/testdata.txt', mode='w')
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
    listFileInfo = ReadFileDatas()
    # shuffle dataset
    random.shuffle(listFileInfo)
    WriteDatasToFile(listFileInfo)
